import os

import requests
import streamlit as st

BACKEND_URL = os.environ["BACKEND_URL"]

st.title("Mini Marketplace")

try:
    response = requests.get(f"{BACKEND_URL}/listings", timeout=5)
except requests.RequestException:
    st.error("Backend niedostępny — serwer API nie odpowiada.")
    st.stop()

if response.status_code == 503:
    st.warning("Backend działa, ale baza danych jest niedostępna.")
elif response.status_code != 200:
    st.error(f"Błąd backendu: kod {response.status_code}")
else:
    st.dataframe(response.json())
