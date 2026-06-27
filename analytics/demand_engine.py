import pandas as pd



def analyze_demand(df):


    df = df.copy()



    # =====================
    # DATE CLEANING
    # =====================


    df["Date"] = pd.to_datetime(

        df["Date"],

        errors="coerce"

    )


    df = df.dropna(

        subset=["Date"]

    )



    revenue = (

        "Net_Revenue"

        if "Net_Revenue" in df.columns

        else "Total_Billed"

    )



    # =====================
    # PEAK HOUR
    # =====================


    df["Hour"] = (

        df["Date"]

        .dt.hour

    )



    hourly = (

        df.groupby("Hour")

        [revenue]

        .mean()

    )



    peak_hour = (

        hourly

        .idxmax()

    )



    # =====================
    # BEST MEAL
    # =====================


    if "Meal_Period" in df.columns:


        best_meal = (

            df.groupby("Meal_Period")

            [revenue]

            .sum()

            .idxmax()

        )


    else:


        best_meal="Unknown"




    # =====================
    # BEST PRODUCT
    # =====================


    if "Item_Name" in df.columns:


        best_item=(

            df.groupby("Item_Name")

            ["Quantity"]

            .sum()

            .idxmax()

        )


    else:


        best_item="Unknown"




    # =====================
    # DEMAND SCORE
    # =====================


    weekend_sales=(

        df[

            df["Date"]

            .dt.dayofweek

            .isin([5,6])

        ]

        [revenue]

        .mean()

    )



    normal_sales=(

        df[

            ~

            df["Date"]

            .dt.dayofweek

            .isin([5,6])

        ]

        [revenue]

        .mean()

    )



    score=(

        weekend_sales

        /

        max(normal_sales,1)

    )*80



    score=min(

        score,

        100

    )





    return {


        "Peak Hour":

            f"{peak_hour}:00",


        "Best Meal":

            best_meal,


        "Best Item":

            best_item,


        "Demand Score":

            round(score,2)

    }