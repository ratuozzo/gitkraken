import krakenex
from pykrakenapi import KrakenAPI
from pandas import DataFrame
import streamlit as st


class KrakenApi:
    def __init__(self):
        try:
            self.api = krakenex.API()
            self.client = KrakenAPI(self.api)
        except Exception as e:
            st.error("Error connecting to API", icon="🚨")

    @st.cache
    def get_tradable_assets_pais(self) -> DataFrame:
        try:
            return self.client.get_tradable_asset_pairs()
        except Exception as e:
            st.error("Error getting assets", icon="🚨")

    @st.cache
    def get_ohlc_data(self, pair: str, interval: int = 1) -> DataFrame:
        try:
            return self.client.get_ohlc_data(pair, interval)[0]
        except Exception as e:
            st.error("Error getting asset data", icon="🚨")
