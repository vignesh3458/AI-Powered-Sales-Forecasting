import pandas as pd

from backend.database import get_sales_data


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    df = get_sales_data()

    if df is None or df.empty:
        return pd.DataFrame()

    return df


# ==========================================
# SUMMARY
# ==========================================

def get_summary():

    df = load_data()

    if df.empty:

        return {

            "total_revenue": 0,

            "net_revenue": 0,

            "transactions": 0,

            "items_sold": 0,

            "average_order_value": 0

        }

    return {

        "total_revenue": float(df["Total_Billed"].sum()),

        "net_revenue": float(df["Net_Revenue"].sum()),

        "transactions": int(len(df)),

        "items_sold": int(df["Quantity"].sum()),

        "average_order_value": round(
            float(df["Total_Billed"].mean()),
            2
        )

    }


# ==========================================
# MONTHLY SALES
# ==========================================

def get_monthly_sales():

    df = load_data()

    if df.empty:
        return []

    monthly = (

        df.groupby("YearMonth")["Total_Billed"]

        .sum()

        .reset_index()

    )

    monthly.columns = [

        "month",

        "sales"

    ]

    return monthly.to_dict(
        orient="records"
    )


# ==========================================
# CATEGORY SALES
# ==========================================

def get_category_sales():

    df = load_data()

    if df.empty:
        return []

    category = (

        df.groupby("Category")["Total_Billed"]

        .sum()

        .reset_index()

        .sort_values(
            "Total_Billed",
            ascending=False
        )

    )

    category.columns = [

        "category",

        "sales"

    ]

    return category.to_dict(
        orient="records"
    )


# ==========================================
# PAYMENT SUMMARY
# ==========================================

def get_payment_summary():

    df = load_data()

    if df.empty:
        return []

    payment = (

        df.groupby("Payment_Method")["Total_Billed"]

        .sum()

        .reset_index()

    )

    payment.columns = [

        "payment_method",

        "sales"

    ]

    return payment.to_dict(
        orient="records"
    )


# ==========================================
# TOP PRODUCTS
# ==========================================

def get_top_products(limit=10):

    df = load_data()

    if df.empty:
        return []

    products = (

        df.groupby("Item_Name")["Quantity"]

        .sum()

        .reset_index()

        .sort_values(
            "Quantity",
            ascending=False
        )

        .head(limit)

    )

    products.columns = [

        "product",

        "quantity"

    ]

    return products.to_dict(
        orient="records"
    )