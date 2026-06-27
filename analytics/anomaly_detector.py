import pandas as pd

import numpy as np



def detect_anomalies(df):


    df=df.copy()


    # ======================
    # DATE
    # ======================


    df["Date"]=pd.to_datetime(

        df["Date"],

        errors="coerce"

    )


    df=df.dropna(

        subset=["Date"]

    )



    revenue=(

        "Net_Revenue"

        if "Net_Revenue" in df.columns

        else "Total_Billed"

    )



    # ======================
    # DAILY REVENUE
    # ======================


    daily=(

        df.groupby(

            df["Date"].dt.floor("D")

        )

        [revenue]

        .sum()

        .reset_index()

    )


    daily.columns=[

        "Date",

        "Revenue"

    ]



    # ======================
    # STATISTICAL LIMITS
    # ======================


    mean=daily["Revenue"].mean()


    std=daily["Revenue"].std()



    upper_limit=(

        mean

        +

        2*std

    )



    lower_limit=(

        mean

        -

        2*std

    )



    # ======================
    # STATUS
    # ======================


    def status(value):


        if value > upper_limit:


            return "High Sales Spike 📈"



        elif value < lower_limit:


            return "Revenue Drop 📉"



        else:


            return "Normal"



    daily["Status"]=(

        daily["Revenue"]

        .apply(status)

    )



    anomalies=(

        daily[

            daily["Status"]!="Normal"

        ]

    )



    return anomalies