from models.trading_pair import TradingPair, pd
import pandas as pd


def get_example_df():
    example_df = """
    {"time":{"1672272000000":1672272000,"1672185600000":1672185600,"1672099200000":1672099200,"1672012800000":1672012800,"1671926400000":1671926400},"open":{"1672272000000":1189.52,"1672185600000":1211.14,"1672099200000":1227.73,"1672012800000":1218.18,"1671926400000":1220.28},"high":{"1672272000000":1191.04,"1672185600000":1214.38,"1672099200000":1232.83,"1672012800000":1230.42,"1671926400000":1223.78},"low":{"1672272000000":1188.87,"1672185600000":1180.5,"1672099200000":1201.0,"1672012800000":1210.43,"1671926400000":1193.78},"close":{"1672272000000":1190.75,"1672185600000":1189.29,"1672099200000":1211.15,"1672012800000":1227.75,"1671926400000":1218.18},"vwap":{"1672272000000":1189.68,"1672185600000":1195.3,"1672099200000":1213.55,"1672012800000":1219.65,"1671926400000":1211.88},"volume":{"1672272000000":219.53628743,"1672185600000":23018.63573815,"1672099200000":10850.00307573,"1672012800000":6613.54923729,"1671926400000":7813.93932945},"count":{"1672272000000":264,"1672185600000":14075,"1672099200000":8826,"1672012800000":5671,"1671926400000":7644}}
    """
    example_df = pd.read_json(example_df, orient="index")
    example_df = example_df.transpose()
    example_df["time"] = example_df["time"].astype(int)
    example_df["time"] = pd.to_datetime(
        example_df["time"], unit="s", origin="unix"
    ).dt.date
    example_df = example_df.sort_index(ascending=True)
    return example_df


# custom constructor for testing
class TestTradingPair(TradingPair):
    def __init__(self, selected_pair: str, interval: int = 1):
        self.pair = selected_pair
        self.interval = interval
        self.ohlc_data = get_example_df()


def test_get_ohlc_data():
    tp = TestTradingPair("ETH_TEST/USD")
    assert tp.get_ohlc_data().to_json() == get_example_df().to_json()


def test_get_moving_average_data():
    tp = TestTradingPair("ETH_TEST/USD")
    assert int(tp.get_moving_average_data(5)["SMA5"][0]) == int(1207.424)


def test_get_rsi_data():
    tp = TestTradingPair("ETH_TEST/USD")
    print(tp.get_rsi_data(2))
    assert tp.get_rsi_data(4).to_json() == get_example_df().to_json()


def test_get_pair():
    tp = TestTradingPair("ETH_TEST/USD")
    assert tp.pair == "ETH_TEST/USD"
