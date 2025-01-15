import streamlit as st
import streamlit as st
import pandas as pd
import FinanceDataReader as fdr # 삼성전자 → 종목코드를 알려주지 않음
import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO # 바이너리 파일들을 읽고 쓸 때 사용하는 패키지
import plotly.graph_objects as go
import pandas as pd

# caching
# 인자가 바뀌지 않는 함수 실행 결과를 저장 후 크롬의 임시 저장 폴더에 저장 후 재사용
@st.cache_data
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    # 이 페이지에서 상장 목록을 받는다.
    method = "download" # 다운로드의 방법으로
    url = "{0}?method={1}".format(base_url, method)   # 0번 자리에 {base_url} 1번자리에 {다운로드}
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     # 6자리로 정리할 것이다.
    df = df[['회사명','종목코드']]  # 데이터 프레임에서 필요로 하는 것만 정리한다.
    return df

def get_ticker_symbol(company_name):
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values
    ticker_symbol = code
    return ticker_symbol

# stock_name을 입력받는 input창 필요
stock_name = st.sidebar.text_input('회사 이름을 입력하세요 : ')
ticker_symbol = get_ticker_symbol(stock_name) # 회사명으로 티커 심벌 반환

today = datetime.datetime.now() # 현재 날짜
this_year = today.year
jan_1 = datetime.date(this_year, 1, 1)

date_range = st.sidebar.date_input(
    "시작일과 종료일을 입력하세요",
    (jan_1, today), # 디폴트값
    jan_1,
    today,
    format="YYYY.MM.DD",
)

accept = st.sidebar.button('확인') # True 리턴

if accept:
    start_p = date_range[0]
    end_p = date_range[1] + datetime.timedelta(days=1) # 오늘까지의 정보를 받고 싶기 때문에 (days=1)

    df = fdr.DataReader(f'KRX:{ticker_symbol[0]}', start_p, end_p)

    df.index = df.index
    st.subheader(f"[{stock_name}] 주가 데이터")
    st.dataframe(df.tail(7))

    excel_data = BytesIO()

    df.to_excel(excel_data)
    st.download_button("엑셀 파일 다운로드",
            excel_data, file_name='stock_data.xlsx')