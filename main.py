import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from models.kraken_api import KrakenApi
from models.trading_pair import TradingPair

api = KrakenApi()

pairs = api.get_tradable_assets_pais()

intervals = {
    1: "1 min",
    5: "5 min",
    15: "15 min",
    30: "30 min",
    60: "1 hour",
    240: "4 hour",
    1440: "1 day",
    10080: "1 week",
    21600: "2 weeks",
}
default_interval = 21600
default_pair = "ETH/USD"

with st.sidebar:
    interval = st.sidebar.selectbox(
        "Select chart interval",
        options=intervals.keys(),
        format_func=lambda x: intervals.get(x),
        index=list(intervals.keys()).index(default_interval),
    )
    selected_pair = st.sidebar.selectbox(
        "Select the trade pair",
        pairs["wsname"],
        index=list(pairs["wsname"]).index(default_pair),
    )


st.title("Kraken API")

time.sleep(1)

selected_pair = TradingPair(selected_pair, interval=interval)


fig = go.Figure()
fig.add_trace(
    go.Candlestick(
        x=selected_pair.ohlc_data["time"],
        open=selected_pair.ohlc_data["open"],
        high=selected_pair.ohlc_data["high"],
        low=selected_pair.ohlc_data["low"],
        close=selected_pair.ohlc_data["close"],
    )
)

with st.container():
    st.header("Kraken data for" + " " + selected_pair.get_pair())

    st.header("Candlestick chart")
    st.plotly_chart(fig, use_container_width=True)

    st.header("Raw data")
    st.dataframe(selected_pair.ohlc_data)
