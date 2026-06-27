def explain_forecast(
        forecast
):


    # ==================================
    # EMPTY FORECAST SAFETY
    # ==================================


    if forecast is None or forecast.empty:


        return {


            "Predicted Revenue": 0,


            "Forecast Range": "0 - 0",


            "Confidence": "Unavailable",


            "Confidence Score": 0,


            "Uncertainty %": 0


        }






    # ==================================
    # REQUIRED COLUMN CHECK
    # ==================================


    required_columns = [


        "yhat",


        "yhat_lower",


        "yhat_upper"


    ]



    for col in required_columns:


        if col not in forecast.columns:


            return {


                "Predicted Revenue": 0,


                "Forecast Range": "Unavailable",


                "Confidence": "Unavailable",


                "Confidence Score": 0,


                "Uncertainty %": 0


            }









    # ==================================
    # GET LATEST FORECAST
    # ==================================


    latest = (

        forecast

        .tail(1)

    )






    prediction = max(

        0,

        float(

            latest["yhat"]

            .iloc[0]

        )

    )






    upper = max(

        0,

        float(

            latest["yhat_upper"]

            .iloc[0]

        )

    )






    lower = max(

        0,

        float(

            latest["yhat_lower"]

            .iloc[0]

        )

    )









    # ==================================
    # UNCERTAINTY CALCULATION
    # ==================================


    if prediction > 0:


        uncertainty = (


            (

                upper

                -

                lower

            )


            /


            prediction


        ) * 100



    else:


        uncertainty = 100







    # Prevent unrealistic values

    uncertainty = min(

        uncertainty,

        100

    )









    # ==================================
    # CONFIDENCE SCORE
    # ==================================


    confidence_score = (

        100

        -

        uncertainty

    )





    confidence_score = max(

        0,

        confidence_score

    )








    # ==================================
    # CONFIDENCE LABEL
    # ==================================


    if confidence_score >= 80:


        confidence = "High"



    elif confidence_score >= 60:


        confidence = "Medium"



    else:


        confidence = "Low"










    # ==================================
    # FINAL BUSINESS OUTPUT
    # ==================================


    explanation = {


        "Predicted Revenue":


            round(

                prediction,

                2

            ),






        "Forecast Range":


            (

                f"{round(lower,2)}"

                +

                " - "

                +

                f"{round(upper,2)}"

            ),






        "Confidence":


            confidence,






        "Confidence Score":


            round(

                confidence_score,

                2

            ),






        "Uncertainty %":


            round(

                uncertainty,

                2

            )


    }






    return explanation