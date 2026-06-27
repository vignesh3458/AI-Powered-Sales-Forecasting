import pandas as pd
import os
import sys
import gc


sys.path.append(
    os.path.abspath(".")
)


from database.company_adapter import (
    prepare_company_data
)



file = "data/Sample Forecast Data.xlsx"



print("Reading Bills...")


bills = pd.read_excel(

    file,

    sheet_name="Bills_Payments",

    engine="calamine"

)



print(
    "Bills:",
    len(bills)
)





print("Reading 2024 Items...")


item_2024 = pd.read_excel(

    file,

    sheet_name="Item Details - 2024",

    engine="calamine"

)



print(
    "2024:",
    len(item_2024)
)






print("Reading 2025 Items...")


item_2025 = pd.read_excel(

    file,

    sheet_name="Item Details - 2025",

    engine="calamine"

)


print(
    "2025:",
    len(item_2025)
)





print("Combining items...")


items = pd.concat(

    [
        item_2024,
        item_2025
    ],

    ignore_index=True

)


del item_2024
del item_2025

gc.collect()






print("Preparing dashboard data...")


df = prepare_company_data(

    bills,

    items

)






# =========================
# SAFETY CHECK
# =========================


if "Net_Revenue" not in df.columns:


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





# =========================
# SORT FOR FORECAST
# =========================


df = df.sort_values(

    "Date"

)






# =========================
# OPTIMIZE MEMORY
# =========================


for col in df.select_dtypes(
    include="object"
).columns:


    if df[col].nunique() < 500:


        df[col] = (

            df[col]

            .astype("category")

        )






del bills
del items

gc.collect()






print("Saving parquet...")


os.makedirs(

    "processed_data",

    exist_ok=True

)



df.to_parquet(

    "processed_data/sales_data.parquet",

    compression="snappy",

    index=False

)




print("DONE")


print(

    "Final Rows:",

    len(df)

)


print(

    "Final Net Revenue:",

    df["Net_Revenue"].sum()

)