from datetime import datetime


def transform_bill_to_sales(bill: dict, item: dict):

    bill_date = bill["bill_date"]

    # -------------------------
    # Meal Period
    # -------------------------

    hour = bill_date.hour

    if hour < 11:
        meal = "Breakfast"
    elif hour < 16:
        meal = "Lunch"
    elif hour < 22:
        meal = "Dinner"
    else:
        meal = "Late Night"

    # -------------------------
    # Revenue
    # -------------------------

    gross_sales = item["quantity"] * item["item_rate"]

    net_sales = gross_sales - item["discount_amount"]

    # -------------------------
    # Analytics Record
    # -------------------------

    return {

        "BillNo": bill["bill_no"],

        "OrderNo": bill["bill_no"],

        "Date": bill_date,

        "ServiceType": bill["service_type"],

        "OrderSource": bill["order_source"],

        "Category": item["category"],

        "Item_Name": item["item_name"],

        "MenuGroup": item["menu_group"],

        "Quantity": item["quantity"],

        "Unit_Price": item["item_rate"],

        "Gross_Sales": gross_sales,

        "Discount_Amt": item["discount_amount"],

        "Net_Sales": net_sales,

        "Tax_Amt": bill["tax_amount"],

        "Total_Billed": bill["total_billed"],

        "Net_Revenue": bill["net_revenue"],

        "Payment_Method": bill["payment_method"],

        "Table_No": bill["table_no"],

        "NoOfPax": bill["no_of_pax"],

        "Year": bill_date.year,

        "Month": bill_date.month,

        "Day": bill_date.day,

        "Week": bill_date.isocalendar().week,

        "YearMonth": bill_date.strftime("%Y-%m"),

        "Day_Name": bill_date.strftime("%A"),

        "Month_Name": bill_date.strftime("%B"),

        "Hour": bill_date.hour,

        "Meal_Period": meal,

        "Weather": bill.get("weather", "Unknown"),

        "Is_Holiday": False,

        "Is_Weekend": bill_date.weekday() >= 5

    }