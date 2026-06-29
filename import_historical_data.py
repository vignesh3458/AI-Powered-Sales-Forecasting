import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# PostgreSQL Connection
# -----------------------------
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/sales_forecast_db"

engine = create_engine(DATABASE_URL)

# -----------------------------
# Read CSV
# -----------------------------
df = pd.read_csv("data/Sample Forecast Data.csv")
# Use only the first 100000 rows for presentation
df = df.head(50000)
# -----------------------------
# Rename Columns
# -----------------------------
df = df.rename(columns={
    "BillorOrderDateTime": "Date",
    "ItemName": "Item_Name",
    "ClassificationName": "Category",
    "MenugroupName": "MenuGroup",
    "ItemRate": "Unit_Price",
    "OrderAmount": "Gross_Sales",
    "DiscountAmount": "Discount_Amt",
    "Revenue": "Net_Sales",
    "TotalTaxAmount": "Tax_Amt",
    "BillAmount": "Total_Billed",
    "SettlAmount": "Net_Revenue",
    "PaymentMode": "Payment_Method",
    "TableNo": "Table_No"
})

df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")
df["Day_Name"] = df["Date"].dt.day_name()
df["Month_Name"] = df["Date"].dt.month_name()
df["Hour"] = df["Date"].dt.hour

df["Meal_Period"] = df["Hour"].apply(
    lambda h: "Breakfast" if h < 11
    else "Lunch" if h < 16
    else "Snacks" if h < 19
    else "Dinner"
)

df["Weather"] = "Normal"
df["Is_Holiday"] = False

df["Is_Weekend"] = df["Day_Name"].isin(
    ["Saturday", "Sunday"]
).astype(bool)

required_columns = [
    "BillNo",
    "OrderNo",
    "Date",
    "ServiceType",
    "OrderSource",
    "Category",
    "Item_Name",
    "MenuGroup",
    "Quantity",
    "Unit_Price",
    "Gross_Sales",
    "Discount_Amt",
    "Net_Sales",
    "Tax_Amt",
    "Total_Billed",
    "Net_Revenue",
    "Payment_Method",
    "Table_No",
    "NoOfPax",
    "Year",
    "Month",
    "Day",
    "Week",
    "YearMonth",
    "Day_Name",
    "Month_Name",
    "Hour",
    "Meal_Period",
    "Weather",
    "Is_Holiday",
    "Is_Weekend"
]

df = df[required_columns]

print(df.columns.tolist())
print(df.head())
print("Rows to import:", len(df))
# -----------------------------
# Upload
# -----------------------------
df.to_sql(
    "restaurant_sales",
    engine,
    if_exists="append",
    index=False
)

print("Historical data imported successfully.")