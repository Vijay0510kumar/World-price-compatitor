import streamlit as st
from app.main import get_prices
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title=" Global Price Comparator", layout="wide")

st.title("🌍 Global Price Comparison Tool (Groq LLM)")
st.markdown(" Compare prices for any product across all major websites and countries using Groq-powered LLM.")

query = st.text_input("Enter product name", "iPhone 16 Pro, 128GB")
country = st.text_input("Enter country name (e.g., US, India, UK, Germany)", "US")
groq_api_key = st.text_input("Enter your Groq API Key", type="password")

if st.button("Compare Prices"):
    if not query or not country or not groq_api_key:
        st.warning("Please provide all inputs.")
    else:
        with st.spinner("Fetching and matching product info..."):
            results = get_prices(query, country, groq_api_key)
            if results:
                st.success(f"Found {len(results)} results:")
                st.dataframe(pd.DataFrame(results))
            else:
                st.error("No matching products found.")