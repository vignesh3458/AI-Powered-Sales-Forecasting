import requests
import pandas as pd
import numpy as np

API_URL = "http://127.0.0.1:8000/sales?limit=100000"


def load_data():


    try:


        response = requests.get(

            API_URL,

            timeout=10

        )


        response.raise_for_status()


    except Exception as e:


        raise Exception(

            f"API connection failed: {e}"

        )



    json_data = response.json()

    df = pd.DataFrame(
        json_data["data"]
    )

    if df.empty:


        raise ValueError(

            "No sales data received from API"

        )
    # -------------------------
    # CLEAN API DATA
    # -------------------------

    df = df.replace(
        {
            np.nan: None
        }
    )


    # Date conversion

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )


    # Numeric cleaning

    numeric_cols = [

        "Year",

        "Month",

        "Quantity",

        "Total_Billed",

        "Net_Revenue",

        "Discount_Amt",

        "Service_Charge",

        "Delivery_Charge",

        "CGST",

        "SGST"

    ]


    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(

                df[col],

                errors="coerce"

            )


    # Remove empty years

    if "Year" in df.columns:

        df = df.dropna(

            subset=["Year"]

        )


        df["Year"] = (

            df["Year"]

            .astype(int)

        )

    if "Net_Revenue" not in df.columns:


        gst = 0


        if "CGST" in df.columns:

            gst += df["CGST"]


        if "SGST" in df.columns:

            gst += df["SGST"]



        df["Net_Revenue"] = (

            df["Total_Billed"]

            -

            gst

        )

    df["Day_Of_Week"] = (

        df["Date"]

        .dt.dayofweek

    )



    df["Month_Start"] = (

        df["Date"]

        .dt.is_month_start

        .astype(int)

    )



    df["Month_End"] = (

        df["Date"]

        .dt.is_month_end

        .astype(int)

    )
    return df