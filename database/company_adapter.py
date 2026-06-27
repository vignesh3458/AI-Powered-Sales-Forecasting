import pandas as pd




def prepare_company_data(
        bills,
        items
):


    # =========================
    # MERGE BILL + ITEM DATA
    # =========================


    df = items.merge(

        bills,

        on="BillNo",

        how="left"

    )






    # =========================
    # RENAME COLUMNS
    # =========================


    df = df.rename(

        columns={


            "BillDateTime":

                "Date",


            "ItemName":

                "Item_Name",


            "ClassificationName":

                "Category",


            "BillAmount":

                "Total_Billed",


            "PaymentMode":

                "Payment_Method",


            "TotalDiscountAmount":

                "Discount_Amt",


            "TotalChargeAmount":

                "Service_Charge"

        }

    )








    # ==================================
    # FIX DUPLICATED BILL VALUES
    # IMPORTANT AFTER ITEM MERGE
    # ==================================


    bill_level_columns = [

        "Total_Billed",

        "Discount_Amt",

        "Service_Charge",

        "TotalTaxAmount"

    ]




    for col in bill_level_columns:


        if col in df.columns:


            df[col] = (

                df.groupby("BillNo")[col]

                .transform(

                    lambda x:

                    [x.iloc[0]]

                    +

                    [0] *

                    (len(x)-1)

                )

            )








    # =========================
    # DATE CLEANING
    # =========================


    df["Date"] = pd.to_datetime(

        df["Date"],

        errors="coerce"

    )



    df = df.dropna(

        subset=[

            "Date"

        ]

    )








    # =========================
    # DATE FEATURES
    # =========================


    df["Year"] = (

        df["Date"]

        .dt.year

    )



    df["Month"] = (

        df["Date"]

        .dt.month

    )



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

        .dt.weekday

        .isin([5,6])

        .astype(int)

    )








    # =========================
    # MEAL PERIOD
    # =========================


    hour = (

        df["Date"]

        .dt.hour

    )




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








    # =========================
    # GST SPLIT
    # =========================


    if "TotalTaxAmount" in df.columns:


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



    else:


        df["CGST"] = 0


        df["SGST"] = 0







    # =========================
    # DEFAULT MONEY COLUMNS
    # =========================


    money_cols = [

        "Total_Billed",

        "Discount_Amt",

        "Service_Charge",

        "CGST",

        "SGST"

    ]




    for col in money_cols:


        if col not in df.columns:


            df[col] = 0




        df[col] = (

            pd.to_numeric(

                df[col],

                errors="coerce"

            )

            .fillna(0)

        )








    # =========================
    # DELIVERY
    # =========================


    if "Delivery_Charge" not in df.columns:


        df["Delivery_Charge"] = 0

        df["Delivery_Charge"] = (

    pd.to_numeric(

        df["Delivery_Charge"],

        errors="coerce"

    )

    .fillna(0)

)







    # =========================
    # NET REVENUE
    # =========================


    df["Net_Revenue"] = (

        df["Total_Billed"]

        -

        df["CGST"]

        -

        df["SGST"]

        -

        df["Discount_Amt"]

        +

        df["Service_Charge"]

        +

        df["Delivery_Charge"]

    )


    df["Net_Revenue"] = (

        df["Net_Revenue"]

        .clip(lower=0)

    )

    # =========================
    # QUANTITY SAFETY
    # =========================


    if "Quantity" in df.columns:


        df["Quantity"] = (

            pd.to_numeric(

                df["Quantity"],

                errors="coerce"

            )

            .fillna(0)

        )


    else:


        df["Quantity"] = 0







    # =========================
    # DEFAULT FEATURES
    # =========================


    if "Weather" not in df.columns:


        df["Weather"] = "Unknown"



    if "Payment_Method" not in df.columns:


        df["Payment_Method"] = "Unknown"









    # =========================
    # STRING OPTIMIZATION
    # =========================


    object_cols = (

        df.select_dtypes(

            include="object"

        )

        .columns

    )



    for col in object_cols:


        df[col] = (

            df[col]

            .fillna("Unknown")

            .astype(str)

        )






    # =========================
    # FORECAST FEATURES
    # =========================


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

