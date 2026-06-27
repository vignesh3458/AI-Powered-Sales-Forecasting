from backend.database import get_sales_data


def get_summary():

    df = get_sales_data()

    return {

        "total_revenue": float(
            df["Total_Billed"].sum()
        ),

        "net_revenue": float(
            df["Net_Revenue"].sum()
        ),

        "transactions": int(
            len(df)
        ),

        "items_sold": int(
            df["Quantity"].sum()
        ),

        "average_order_value": round(

            float(df["Total_Billed"].mean()),

            2

        )

    }