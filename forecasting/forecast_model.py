import pandas as pd

import numpy as np

import streamlit as st


from xgboost import XGBRegressor



# ===================================
# XGBOOST FORECAST CACHE
# ===================================


@st.cache_data(
    ttl=86400,
    show_spinner=False
)


def generate_forecast(
        df,
        model_version=None,
        periods=30,
        category="All"
):


    df = df.copy()


    _ = model_version



    # ==========================
    # CATEGORY FILTER
    # ==========================


    if (

        category != "All"

        and

        "Category" in df.columns

    ):


        df = df[

            df["Category"] == category

        ]



    # ==========================
    # DATE CLEANING
    # ==========================


    df["Date"] = pd.to_datetime(

        df["Date"],

        errors="coerce"

    )


    df = df.dropna(

        subset=["Date"]

    )



    # ==========================
    # REVENUE COLUMN
    # ==========================


    revenue = (

        "Net_Revenue"

        if "Net_Revenue" in df.columns

        else "Total_Billed"

    )



    df[revenue] = pd.to_numeric(

        df[revenue],

        errors="coerce"

    ).fillna(0)



    df = df[

        df[revenue] > 0

    ]



    # ==========================
    # DAILY AGGREGATION
    # ==========================


    data = (

        df.groupby(

            df["Date"].dt.floor("D")

        )

        [revenue]

        .sum()

        .reset_index()

    )


    data.columns = [

        "ds",

        "y"

    ]



    data = (

        data

        .sort_values("ds")

        .reset_index(drop=True)

    )



    # ==========================
    # REMOVE OUTLIERS
    # ==========================


    low = data["y"].quantile(0.02)


    high = data["y"].quantile(0.98)



    data["y"] = (

        data["y"]

        .clip(

            low,

            high

        )

    )



    # ==========================
    # FEATURE ENGINEERING
    # ==========================


    def create_features(data):


        data = data.copy()


        data["day"] = (

            data["ds"]

            .dt.day

        )


        data["month"] = (

            data["ds"]

            .dt.month

        )


        data["year"] = (

            data["ds"]

            .dt.year

        )


        data["weekday"] = (

            data["ds"]

            .dt.dayofweek

        )


        data["is_weekend"] = (

            data["weekday"]

            .isin([5,6])

            .astype(int)

        )


        for lag in [

            1,

            7,

            14,

            30

        ]:


            data[f"lag_{lag}"] = (

                data["y"]

                .shift(lag)

            )



        data["rolling_7"] = (

            data["y"]

            .rolling(7)

            .mean()

        )


        data["rolling_14"] = (

            data["y"]

            .rolling(14)

            .mean()

        )


        data["rolling_30"] = (

            data["y"]

            .rolling(30)

            .mean()

        )


        return data




    data = create_features(data)


    data = data.dropna()



    # ==========================
    # MODEL FEATURES
    # ==========================


    features = [


        "day",

        "month",

        "year",

        "weekday",

        "is_weekend",


        "lag_1",

        "lag_7",

        "lag_14",

        "lag_30",


        "rolling_7",

        "rolling_14",

        "rolling_30"

    ]



    X = data[features]


    y = np.log1p(

        data["y"]

    )



    # ==========================
    # XGBOOST MODEL
    # ==========================


    model = XGBRegressor(


        n_estimators=3000,


        learning_rate=0.01,


        max_depth=5,


        min_child_weight=5,


        subsample=0.85,


        colsample_bytree=0.85,


        objective="reg:squarederror",


        random_state=42


    )



    model.fit(

        X,

        y

    )



    # ==========================
    # FUTURE PREDICTION
    # ==========================


    history = data[

        [

            "ds",

            "y"

        ]

    ].copy()



    predictions = []



    error_margin = (

        history["y"]

        .std()

        *

        0.15

    )



    for i in range(periods):


        next_date = (

            history["ds"].max()

            +

            pd.Timedelta(days=1)

        )



        future_row = pd.DataFrame(

            {

                "ds":[next_date],

                "y":[history["y"].iloc[-1]]

            }

        )



        temp = pd.concat(

            [

                history,

                future_row

            ],

            ignore_index=True

        )



        temp = create_features(temp)



        row = temp.tail(1)



        pred = model.predict(

            row[features]

        )[0]



        pred = np.expm1(

            pred

        )



        pred = max(

            pred,

            0

        )



        # ======================
        # CONFIDENCE RANGE
        # ======================


        lower = max(

            pred - error_margin,

            0

        )



        upper = (

            pred

            +

            error_margin

        )



        if pred > 0:


            confidence = (

                100

                -

                (

                    error_margin

                    /

                    pred

                    *

                    100

                )

            )


        else:


            confidence = 0



        confidence = max(

            0,

            min(

                confidence,

                100

            )

        )



        predictions.append(

            {


                "ds":

                    next_date,


                "yhat":

                    round(pred,2),


                "yhat_lower":

                    round(lower,2),


                "yhat_upper":

                    round(upper,2),


                "Confidence":

                    round(confidence,2)


            }

        )



        history = pd.concat(

            [

                history,


                pd.DataFrame(

                    {

                        "ds":[next_date],

                        "y":[pred]

                    }

                )

            ],

            ignore_index=True

        )



    forecast = pd.DataFrame(

        predictions

    )



    forecast["Revenue_Type"] = (

        "XGBoost AI Forecast"

    )



    return forecast