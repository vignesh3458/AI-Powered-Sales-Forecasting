import pandas as pd



def process_sales_data(df):


    df = df.copy()



    # =========================
    # DATE CLEANING
    # =========================


    if "Date" in df.columns:


        df["Date"] = pd.to_datetime(

            df["Date"],

            errors="coerce"

        )


        df = df.dropna(

            subset=["Date"]

        )







    # =========================
    # REQUIRED MONEY COLUMNS
    # =========================


    money_columns = [


        "Gross_Sales",

        "Net_Sales",

        "Total_Billed",

        "Discount_Amt",

        "Tax_Amt",

        "CGST",

        "SGST",

        "Service_Charge",

        "Delivery_Charge"

    ]



    for col in money_columns:


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
    # TAX HANDLING
    # =========================


    # CGST + SGST available


    if df["Tax_Amt"].sum() == 0:


        df["Tax_Amt"] = (

            df["CGST"]

            +

            df["SGST"]

        )




    # Only Tax available


    if (

        df["Tax_Amt"].sum() > 0

        and

        df["CGST"].sum() == 0

        and

        df["SGST"].sum() == 0

    ):


        df["CGST"] = (

            df["Tax_Amt"]

            /

            2

        )


        df["SGST"] = (

            df["Tax_Amt"]

            /

            2

        )









    # =========================
    # NET SALES CREATION
    # =========================


    if df["Net_Sales"].sum() == 0:


        df["Net_Sales"] = (

            df["Gross_Sales"]

            -

            df["Discount_Amt"]

        )









    # =========================
    # TOTAL BILL CREATION
    # =========================


    if df["Total_Billed"].sum() == 0:


        df["Total_Billed"] = (

            df["Net_Sales"]

            +

            df["Tax_Amt"]

            +

            df["Service_Charge"]

            +

            df["Delivery_Charge"]

        )









    # =========================
    # NET REVENUE
    # IMPORTANT FOR FORECAST
    # =========================


    df["Net_Revenue"] = (

        df["Total_Billed"]

        -

        df["CGST"]

        -

        df["SGST"]

    )



    df["Net_Revenue"] = (

        df["Net_Revenue"]

        .clip(

            lower=0

        )

    )








    # =========================
    # QUANTITY
    # =========================


    if "Quantity" not in df.columns:


        df["Quantity"] = 0



    df["Quantity"] = (

        pd.to_numeric(

            df["Quantity"],

            errors="coerce"

        )

        .fillna(0)

    )









    # =========================
    # DATE FEATURES
    # =========================


    if "Date" in df.columns:


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








    # =========================
    # DEFAULT TEXT COLUMNS
    # =========================


    defaults = {


        "Category":"Unknown",

        "Item_Name":"Unknown",

        "Payment_Method":"Unknown",

        "Weather":"Unknown"


    }




    for col,value in defaults.items():


        if col not in df.columns:


            df[col] = value



        df[col] = (

            df[col]

            .fillna(value)

            .astype(str)

        )







    return df