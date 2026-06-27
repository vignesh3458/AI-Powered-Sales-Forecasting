import numpy as np

from backend.analytics_service import (
    get_summary,
    get_monthly_sales,
    get_category_sales,
    get_payment_summary,
    get_top_products
)

from backend.database import get_sales_data


# ==========================================================
# SALES DATA
# ==========================================================

def sales_api(limit=None):

    df = get_sales_data()

    if df.empty:

        return {

            "status": "success",

            "total_records": 0,

            "data": []

        }

    df = df.replace({

        np.nan: None,

        np.inf: None,

        -np.inf: None

    })

    if "Date" in df.columns:
        df["Date"] = df["Date"].astype(str)

        # Convert every NaN/NaT/Infinity to None
        df = df.astype(object)
        df = df.where(df.notna(), None)

        if limit is not None:
            df = df.head(limit)

        return {
            "status": "success",
            "total_records": len(df),
            "data": df.to_dict(orient="records")
        }


# ==========================================================
# SUMMARY
# ==========================================================

def summary_api():

    return {

        "status": "success",

        "data": get_summary()

    }


# ==========================================================
# MONTHLY SALES
# ==========================================================

def monthly_api():

    return {

        "status": "success",

        "data": get_monthly_sales()

    }


# ==========================================================
# CATEGORY SALES
# ==========================================================

def category_api():

    return {

        "status": "success",

        "data": get_category_sales()

    }


# ==========================================================
# PAYMENT SUMMARY
# ==========================================================

def payment_api():

    return {

        "status": "success",

        "data": get_payment_summary()

    }


# ==========================================================
# TOP PRODUCTS
# ==========================================================

def top_products_api():

    return {

        "status": "success",

        "data": get_top_products()

    }