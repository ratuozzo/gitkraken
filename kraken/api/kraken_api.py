import krakenex
from pykrakenapi import KrakenAPI
from pandas import DataFrame
import streamlit as st

class KrakenApi:
    def __init__(self):
        self.api = krakenex.API() 
        self.client = KrakenAPI(self.api)

    @st.cache
    def get_tradable_assets_pais(self)-> DataFrame:
        return self.client.get_tradable_asset_pairs()
    @st.cache
    def get_ohlc_data(self, pair: str, interval: int = 1) -> DataFrame:
        return self.client.get_ohlc_data(pair, interval)[0]