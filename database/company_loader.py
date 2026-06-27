import pandas as pd
import requests
import streamlit as st


# ======================================================
# API URL
# ======================================================

API_URL = "http://127.0.0.1:8000/sales"


@st.cache_data(
    ttl=5,
    show_spinner=False
)

def load_company_data():

    response = requests.get(API_URL)

    if response.status_code != 200:
        raise Exception(
            f"Unable to fetch data from API ({response.status_code})"
        )

    result = response.json()

    df = pd.DataFrame(
        result["data"]
    )

    if df.empty:
        raise ValueError(
            "No data received from API."
        )

    # ==========================
    # DATE
    # ==========================

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    # ==========================
    # NUMERIC COLUMNS
    # ==========================

    numeric_columns = [

        "Total_Billed",

        "Net_Revenue",

        "Quantity",

        "CGST",

        "SGST"

    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    return df