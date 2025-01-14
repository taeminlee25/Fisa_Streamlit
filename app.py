import streamlit as st
import pandas as pd
import numpy as np

title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)