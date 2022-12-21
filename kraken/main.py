from api.kraken_api import KrakenApi
import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd

api = KrakenApi()

pairs =  api.get_tradable_assets_pais()

interval_display_options = (
        '1 min',
        '5 min',
        '15 min',
        '30 min',
        '1 hour',
        '4 hours',
        '1 day',
        '1 week',
        '2 weeks', 
        )

interval_value_options = (
        1,
        5,
        15,
        30,
        60,
        240,
        1440,
        10080,
        21600,
        )

format_function = lambda x: interval_display_options[interval_value_options.index(x)]

with st.sidebar:
    interval = st.sidebar.selectbox(
        "Select chart interval", 
        interval_value_options,
        format_func= format_function
    )

st.title("Kraken API")
st.header("Kraken tradable asset pairs")
 
selected_pair = st.selectbox('Select the trade pair', pairs['wsname'])

time.sleep(1) 

ohlc_data = api.get_ohlc_data(selected_pair, interval=interval)
ohlc_data['time'] = pd.to_datetime(ohlc_data['time'], unit='s', origin='unix').dt.date
fig = go.Figure()
fig.add_trace(go.Candlestick(x=ohlc_data['time'], open=ohlc_data['open'], high=ohlc_data['high'], low=ohlc_data['low'], close=ohlc_data['close']) )

with st.container():
    st.write('Candlestick chart')
    st.plotly_chart(fig, use_container_width=True)

st.header(ohlc_data.columns)

st.dataframe(ohlc_data)

