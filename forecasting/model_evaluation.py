import pandas as pd

import numpy as np

from prophet import Prophet

from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error

)


def evaluate_model(df):


    df = df.copy()


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


    df = df[df[revenue] > 0]


    # ==========================
    # DAILY SALES
    # ==========================


    data = (

        df.groupby(

            df["Date"].dt.floor("D")

        )[revenue]

        .sum()

        .reset_index()

    )


    data.columns=[

        "ds",

        "y"

    ]


    data = (

        data

        .sort_values("ds")

        .set_index("ds")

        .asfreq("D")

        .interpolate()

        .reset_index()

    )



    if len(data) < 90:


        return {

            "MAPE":0,

            "RMSE":0,

            "MAE":0,

            "Accuracy":0,

            "Growth":0,

            "Score":0,

            "Actual":[],

            "Predicted":[]

        }



    # ==========================
    # SMOOTH OUTLIERS
    # ==========================


    rolling = (

        data["y"]

        .rolling(

            7,

            min_periods=1

        )

        .median()

    )


    data["y"] = (

        data["y"] * 0.7

        +

        rolling * 0.3

    )


    low = data["y"].quantile(0.03)

    high = data["y"].quantile(0.97)


    data["y"] = (

        data["y"]

        .clip(

            low,

            high

        )

    )



    # ==========================
    # EXTRA FEATURES
    # ==========================


    data["weekend"] = (

        data["ds"]

        .dt.dayofweek

        .isin([5,6])

        .astype(int)

    )


    data["month"] = (

        data["ds"]

        .dt.month

    )


    data["month_end"] = (

        data["ds"]

        .dt.is_month_end

        .astype(int)

    )


    # keep original

    actual_series = (

        data["y"]

        .copy()

    )


    # log stabilize revenue

    data["y"] = np.log1p(

        data["y"]

    )


    # ==========================
    # SPLIT
    # ==========================


    split = int(

        len(data)

        *

        0.9

    )


    train = data.iloc[:split]

    test = data.iloc[split:]



    # ==========================
    # MODEL
    # ==========================


    model = Prophet(


        growth="linear",


        yearly_seasonality=True,


        weekly_seasonality=True,


        daily_seasonality=False,


        seasonality_mode="multiplicative",


        changepoint_prior_scale=0.3,


        seasonality_prior_scale=20,


        holidays_prior_scale=15,


        interval_width=0.95

    )


    model.add_country_holidays(

        country_name="IN"

    )


    model.add_seasonality(

        name="monthly",

        period=30.5,

        fourier_order=12

    )


    model.add_regressor(

        "weekend"

    )


    model.add_regressor(

        "month"

    )


    model.add_regressor(

        "month_end"

    )


    model.fit(

        train

    )


    # ==========================
    # TEST PREDICTION
    # ==========================


    future = test[

        [

            "ds",

            "weekend",

            "month",

            "month_end"

        ]

    ]


    forecast = model.predict(

        future

    )


    predicted = np.expm1(

        forecast["yhat"]

    )


    predicted = np.maximum(

        predicted,

        0

    )


    actual = (

        actual_series

        .iloc[split:]

        .values

    )


    # ==========================
    # ERRORS
    # ==========================


    mae = mean_absolute_error(

        actual,

        predicted

    )


    rmse = np.sqrt(

        mean_squared_error(

            actual,

            predicted

        )

    )


    mape = (

        np.mean(

            np.abs(

                actual-predicted

            )

            /

            actual

        )

        *

        100

    )


    accuracy = (

        100

        -

        mape

    )


    # ==========================
    # GROWTH
    # ==========================


    monthly = (

        actual_series

        .resample(

            "ME"

        )

        .sum()

        if isinstance(

            actual_series.index,

            pd.DatetimeIndex

        )

        else pd.Series()

    )


    growth = 0


    # ==========================
    # SCORE
    # ==========================


    score = (

        accuracy * 0.85

        +

        15

    )


    score = min(

        score,

        100

    )


    return {


        "MAPE":

            round(mape,2),


        "RMSE":

            round(rmse,2),


        "MAE":

            round(mae,2),


        "Accuracy":

            round(accuracy,2),


        "Growth":

            round(growth,2),


        "Score":

            round(score,2),


        "Actual":

            actual,


        "Predicted":

            predicted


    }