from api.kraken_api import KrakenApi
import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd

api = KrakenApi()

pairs = api.get_tradable_assets_pais()

key_values = {
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

with st.sidebar:
    interval = st.sidebar.selectbox(
        "Select chart interval",
        options=key_values.keys(),
        format_func=lambda x: key_values.get(x),
    )

st.title("Kraken API")
st.header("Kraken tradable asset pairs")

selected_pair = st.selectbox("Select the trade pair", pairs["wsname"])

time.sleep(1)

ohlc_data = api.get_ohlc_data(selected_pair, interval=interval)
ohlc_data["time"] = pd.to_datetime(ohlc_data["time"], unit="s", origin="unix").dt.date
fig = go.Figure()
fig.add_trace(
    go.Candlestick(
        x=ohlc_data["time"],
        open=ohlc_data["open"],
        high=ohlc_data["high"],
        low=ohlc_data["low"],
        close=ohlc_data["close"],
    )
)

with st.container():
    st.write("Candlestick chart")
    st.plotly_chart(fig, use_container_width=True)

st.header(ohlc_data.columns)

st.dataframe(ohlc_data)
