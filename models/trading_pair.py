import pandas as pd
from models.kraken_api import KrakenApi
import streamlit as st


class TradingPair:
    def __init__(self, selected_pair: str, interval: int = 1):
        self.api = KrakenApi()
        try:
            self.pair = selected_pair
            self.ohlc_data = self.api.get_ohlc_data(selected_pair, interval=interval)
            # Format time
            self.ohlc_data["time"] = pd.to_datetime(
                self.ohlc_data["time"], unit="s", origin="unix"
            ).dt.date
            # Sort by time ascending
            self.ohlc_data = self.ohlc_data.sort_index(ascending=True)
        except Exception as e:
            st.error("Error instantiating TradingPair model", icon="🚨")

    def get_ohlc_data(self) -> pd.DataFrame:
        # Return a copy of the dataframe
        df = self.ohlc_data.copy(deep=True)
        return df

    def get_moving_average_data(self, window=30) -> pd.DataFrame:
        df = self.get_ohlc_data()
        # Add moving average column
        try:
            df["SMA" + str(window)] = df["close"].rolling(window).mean()
            df = df[["SMA" + str(window), "close"]]  # drop all other columns
            df = df.dropna()  # drop all rows with null values
            return df
        except Exception as e:
            st.error("Error on get_moving_average_data", icon="🚨")

    def get_rsi_data(self, periods=14) -> pd.DataFrame:
        df = self.get_ohlc_data()
        try:
            close_delta = df["close"].diff()
            # Make two series: one for lower closes and one for higher closes
            up = close_delta.clip(lower=0)
            down = -1 * close_delta.clip(upper=0)

            ma_up = up.rolling(window=periods).mean()
            ma_down = down.rolling(window=periods).mean()

            rsi = ma_up / ma_down
            rsi = 100 - (100 / (1 + rsi))
            return rsi
        except Exception as e:
            st.error("Error on get_rsi_data", icon="🚨")

    def get_pair(self) -> str:
        return self.pair
