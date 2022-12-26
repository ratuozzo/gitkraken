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

    def get_ohlc_data(self) -> pd.DataFrame:
        return self.ohlc_data

    def get_pair(self) -> str:
        return self.pair
