import pandas as pd

import numpy as np


from xgboost import XGBRegressor


from sklearn.metrics import (

    mean_absolute_error,

    mean_squared_error

)





def evaluate_xgboost(df):


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



    df[revenue] = (

        pd.to_numeric(

            df[revenue],

            errors="coerce"

        )

        .fillna(0)

    )



    df = df[

        df[revenue] > 0

    ]






    # ==========================
    # DAILY REVENUE
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

        "Date",

        "Revenue"

    ]



    data = data.sort_values(

        "Date"

    )






    # ==========================
    # SMOOTHING
    # ==========================


    data["Revenue"] = (

        data["Revenue"]

        .rolling(

            3,

            min_periods=1

        )

        .mean()

    )





    low = (

        data["Revenue"]

        .quantile(0.02)

    )


    high = (

        data["Revenue"]

        .quantile(0.98)

    )



    data["Revenue"] = (

        data["Revenue"]

        .clip(

            low,

            high

        )

    )







    # ==========================
    # FEATURE ENGINEERING
    # ==========================


    data["day"] = data["Date"].dt.day


    data["month"] = data["Date"].dt.month


    data["weekday"] = data["Date"].dt.dayofweek



    data["week"] = (

        data["Date"]

        .dt.isocalendar()

        .week

        .astype(int)

    )



    data["weekend"] = (

        data["weekday"]

        .isin([5,6])

        .astype(int)

    )






    for lag in [

        1,

        2,

        3,

        7,

        14,

        30

    ]:


        data[f"lag_{lag}"] = (

            data["Revenue"]

            .shift(lag)

        )





    for window in [

        7,

        14,

        30

    ]:


        data[f"rolling_{window}"] = (

            data["Revenue"]

            .rolling(window)

            .mean()

        )





    data = data.dropna()






    features = [


        "day",

        "month",

        "weekday",

        "week",

        "weekend",


        "lag_1",

        "lag_2",

        "lag_3",

        "lag_7",

        "lag_14",

        "lag_30",


        "rolling_7",

        "rolling_14",

        "rolling_30"

    ]






    X = data[features]


    y = np.log1p(

        data["Revenue"]

    )








    # ==========================
    # TRAIN TEST SPLIT
    # ==========================


    split = int(

        len(data)

        *

        0.9

    )



    X_train = X.iloc[:split]


    X_test = X.iloc[split:]



    y_train = y.iloc[:split]



    actual = (

        data["Revenue"]

        .iloc[split:]

    )









    # ==========================
    # MODEL
    # ==========================


    model = XGBRegressor(


        n_estimators=3500,


        learning_rate=0.008,


        max_depth=5,


        min_child_weight=4,


        subsample=0.85,


        colsample_bytree=0.85,


        objective="reg:squarederror",


        random_state=42

    )




    model.fit(

        X_train,

        y_train

    )






    # ==========================
    # PREDICTION
    # ==========================


    pred = np.expm1(

        model.predict(

            X_test

        )

    )



    pred = np.maximum(

        pred,

        0

    )








    # ==========================
    # METRICS
    # ==========================


    mae = mean_absolute_error(

        actual,

        pred

    )




    rmse = np.sqrt(

        mean_squared_error(

            actual,

            pred

        )

    )





    mape = (

        np.mean(

            np.abs(

                actual - pred

            )

            /

            np.maximum(

                actual,

                1

            )

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
    # AI FORECAST GROWTH
    # ==========================


    recent_actual = (

        data["Revenue"]

        .tail(30)

        .sum()

    )



    future_prediction = (

        pred[-30:]

        .sum()

    )




    growth = (

        (

            future_prediction

            -

            recent_actual

        )

        /

        max(

            recent_actual,

            1

        )

        *

        100

    )









    # ==========================
    # MODEL SCORE
    # ==========================


    stability = (

        100

        -

        min(

            (

                rmse

                /

                actual.mean()

                *

                100

            ),

            100

        )

    )






    score = (

        accuracy * 0.75

        +

        stability * 0.20

        +

        min(

            max(

                growth + 50,

                0

            ),

            100

        )

        *

        0.05

    )








    # ==========================
    # FEATURE IMPORTANCE
    # ==========================


    importance = dict(

        zip(

            features,

            model.feature_importances_

        )

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



        "Importance":

            importance,



        "Actual":

            actual.values,



        "Predicted":

            pred

    }