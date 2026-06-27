import pandas as pd

import os

import gc

from pathlib import Path


from database.universal_loader import load_dataset




# ==========================
# AUTO FIND DATA FILE
# ==========================


data_folder = Path(
    "data"
)



allowed_files = [

    ".csv",

    ".json",

    ".xlsx",

    ".xls",

    ".parquet"

]



files = [

    file

    for file in data_folder.iterdir()

    if file.suffix.lower() in allowed_files

]



if len(files) == 0:


    raise FileNotFoundError(

        "No CSV / JSON / Excel dataset found in data folder"

    )





file = files[0]



print(

    "Reading Dataset:",

    file

)





# ==========================
# UNIVERSAL LOAD
# ==========================


df = load_dataset(

    file

)



print(

    "Rows:",

    len(df)

)


# ==========================
# RENAME COLUMNS
# ==========================


df = df.rename(

    columns={

        "BillorOrderDateTime":
        "Date",


        "BillAmount":
        "Total_Billed",


        "ItemName":
        "Item_Name",


        "ClassificationName":
        "Category",


        "PaymentMode":
        "Payment_Method",


        "TotalDiscountAmount":
        "Discount_Amt",


        "TotalChargeAmount":
        "Service_Charge"

    }

)



# ==========================
# DATE
# ==========================


df["Date"] = pd.to_datetime(

    df["Date"],

    errors="coerce"

)


df = df.dropna(
    subset=["Date"]
)



# ==========================
# NUMBERS
# ==========================


numeric_cols = [

    "Total_Billed",

    "Quantity",

    "TotalTaxAmount",

    "Discount_Amt",

    "Service_Charge"

]


for col in numeric_cols:


    if col in df.columns:


        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        ).fillna(0)



# ==========================
# REMOVE DUPLICATED BILL VALUES
# ==========================


if "BillNo" in df.columns:


    bill_count = (

        df.groupby("BillNo")
        ["BillNo"]
        .transform("count")

    )


    split_columns = [

        "Total_Billed",

        "TotalTaxAmount",

        "Discount_Amt",

        "Service_Charge"

    ]


    for col in split_columns:


        if col in df.columns:


            df[col] = (

                df[col]

                /

                bill_count

            )


    print(
        "Bill level values distributed"
    )

# ==========================
# DELIVERY CHARGE
# ==========================


if "Delivery_Charge" not in df.columns:


    df["Delivery_Charge"] = 0



df["Delivery_Charge"] = (

    pd.to_numeric(

        df["Delivery_Charge"],

        errors="coerce"

    )

    .fillna(0)

)

# ==========================
# GST / TAX HANDLING
# ==========================


if "TotalTaxAmount" in df.columns:


    df["TotalTaxAmount"] = (

        pd.to_numeric(

            df["TotalTaxAmount"],

            errors="coerce"

        )

        .fillna(0)

    )


else:


    df["TotalTaxAmount"] = 0





# Standard Tax Column

df["Tax_Amt"] = (

    df["TotalTaxAmount"]

)



# GST Split

df["CGST"] = (

    df["TotalTaxAmount"]

    /

    2

)



df["SGST"] = (

    df["TotalTaxAmount"]

    /

    2

)



# Dashboard GST KPI / Chart Support

df["GST_Total"] = (

    df["CGST"]

    +

    df["SGST"]

)


# ==========================
# NET REVENUE
# ==========================


df["Net_Revenue"] = (

    df["Total_Billed"]

    -

    df["CGST"]

    -

    df["SGST"]

)


df["Net_Revenue"] = (

    df["Net_Revenue"]

    .clip(lower=0)

)



# ==========================
# DATE FEATURES
# ==========================


df["Year"] = df["Date"].dt.year


df["Month"] = df["Date"].dt.month


df["Month_Name"] = (
    df["Date"]
    .dt.month_name()
)


df["Day_Name"] = (
    df["Date"]
    .dt.day_name()
)


df["YearMonth"] = (

    df["Date"]

    .dt.strftime("%Y-%m")

)


df["Is_Weekend"] = (

    df["Date"]

    .dt.dayofweek

    .isin([5,6])

    .astype(int)

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

# ==========================
# MEAL PERIOD
# ==========================

hour = df["Date"].dt.hour


df["Meal_Period"] = pd.cut(

    hour,

    bins=[
        -1,
        11,
        16,
        23
    ],

    labels=[
        "Breakfast",
        "Lunch",
        "Dinner"
    ]

)


df["Meal_Period"] = (

    df["Meal_Period"]

    .astype(str)

)


# ==========================
# DEFAULTS
# ==========================


for col in [

    "Category",

    "Item_Name",

    "Payment_Method"

]:


    df[col] = (

        df[col]

        .fillna("Unknown")

    )



df["Weather"] = "Unknown"

# ==========================
# QUANTITY SAFETY
# ==========================


if "Quantity" not in df.columns:


    df["Quantity"] = 0


df["Quantity"] = (

    pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    .fillna(0)

)


# ==========================
# OPTIMIZE
# ==========================


for col in df.select_dtypes(

    include=["object","string"]

).columns:


    if df[col].nunique() < 1000:


        df[col] = (

            df[col]

            .astype("category")

        )



gc.collect()



# ==========================
# SAVE
# ==========================


os.makedirs(

    "processed_data",

    exist_ok=True

)



df.to_parquet(

    "processed_data/sales_data.parquet",

    compression="snappy",

    index=False

)



print("====================")
print("PARQUET CREATED")
print("====================")


print(
    "Rows:",
    len(df)
)


print(
    "Total Revenue:",
    df["Total_Billed"].sum()
)


print(
    "Net Revenue:",
    df["Net_Revenue"].sum()
)


print(
    "Dates:",
    df["Date"].min(),
    df["Date"].max()
)

print(

    "GST Total:",

    df["GST_Total"].sum()

)