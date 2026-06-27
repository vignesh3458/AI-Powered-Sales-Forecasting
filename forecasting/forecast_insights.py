import pandas as pd



def generate_forecast_insight(
        forecast,
        df
):


    # =========================
    # SAFETY
    # =========================


    if forecast.empty:


        return {

            "Trend":"Unavailable",

            "Message":"No forecast available",

            "Actions":[]

        }



    # =========================
    # FORECAST CHANGE
    # =========================


    start_value = (

        forecast["yhat"]

        .head(7)

        .mean()

    )


    end_value = (

        forecast["yhat"]

        .tail(7)

        .mean()

    )



    change = (

        (

            end_value

            -

            start_value

        )

        /

        max(
            start_value,
            1
        )

        *

        100

    )




    # =========================
    # TREND
    # =========================


    if change > 5:


        trend = "Growing 📈"


        message = (

            "Revenue is expected to increase"

        )



    elif change < -5:


        trend = "Declining 📉"


        message = (

            "Revenue may decrease"

        )



    else:


        trend = "Stable ➖"


        message = (

            "Revenue expected to remain stable"

        )





    # =========================
    # BUSINESS ACTIONS
    # =========================


    actions=[]



    if trend=="Growing 📈":


        actions.extend(

            [

                "Increase inventory preparation",

                "Plan marketing campaigns",

                "Ensure staff availability"

            ]

        )



    elif trend=="Declining 📉":


        actions.extend(

            [

                "Create promotional offers",

                "Analyze low performing categories",

                "Improve customer engagement"

            ]

        )


    else:


        actions.extend(

            [

                "Maintain current strategy",

                "Monitor demand changes"

            ]

        )





    return {


        "Trend":

            trend,


        "Change":

            round(change,2),


        "Message":

            message,


        "Actions":

            actions

    }