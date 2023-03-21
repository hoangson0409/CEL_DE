import requests
import json
import streamlit as st
import pandas as pd
import plotly.express as px

# Define the title
st.title("Stock Data Web Application")
st.markdown('Enter the stock ticker and duration to display the line chart.')

days = st.select_slider(
    "How many days in the past you want to look into",
    options=["5", "10","15", "20","30","45"]
)

ticker = st.radio(
    "What stock do you want to retrieve data from",
    ('AAPL', 'MSFT', 'GOOG','AMZN','NVDA','TSLA','META','JNJ','WMT','JPM'))

data = {'ticker':ticker,'time_past' : int(days)}

if st.button("Submit"):
    response = requests.post('http://127.0.0.1:8000/stockchart', params=data)
    json_response = response.json()

    stock_data = pd.DataFrame.from_records(json_response)
    fig = px.line(stock_data, x='date', y='close', title=f'{ticker} Stock Data')
    st.plotly_chart(fig)

