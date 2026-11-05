import os

import requests
import streamlit as st

BACKEND_URL = os.environ["BACKEND_URL"]

st.title("Mini Marketplace")

try:
    response = requests.get(f"{BACKEND_URL}/listings", timeout=5)
    response.raise_for_status()
    st.dataframe(response.json())
except requests.RequestException as error:
    st.error(f"Backend niedostępny: {error}")
