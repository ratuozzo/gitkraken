import pandas as pd
from models.kraken_api import KrakenApi


class TradingPair:
    def __init__(self, selected_pair: str, interval: int = 1):
        self.api = KrakenApi()

        self.pair = selected_pair
        self.ohlc_data = self.api.get_ohlc_data(selected_pair, interval=interval)
        # Format time
        self.ohlc_data["time"] = pd.to_datetime(
            self.ohlc_data["time"], unit="s", origin="unix"
        ).dt.date
        self.ohlc_data = self.ohlc_data.sort_index(ascending=True)

    def get_ohlc_data(self) -> pd.DataFrame:
        df = self.ohlc_data.copy(deep=True)
        return df

    def get_moving_average_data(self, window=30) -> pd.DataFrame:
        df = self.get_ohlc_data()
        df["SMA" + str(window)] = df["close"].rolling(window).mean()
        df = df[["SMA" + str(window), "close"]]  # drop all other columns
        df = df.dropna()  # drop all rows with null values
        return df

    def get_rsi_data(self, periods=14) -> pd.DataFrame:
        """
        Returns rsi
        """
        df = self.get_ohlc_data()
        close_delta = df["close"].diff()
        print(close_delta)
        # Make two series: one for lower closes and one for higher closes
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        ma_up = up.rolling(window=periods).mean()
        ma_down = down.rolling(window=periods).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100 / (1 + rsi))
        return rsi

    def get_pair(self) -> str:
        return self.pair
