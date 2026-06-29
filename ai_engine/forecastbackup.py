import ollama

import streamlit as st





# ==================================
# FORECAST AI CONTEXT CACHE
# ==================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)


def prepare_forecast_context(forecast):


    forecast = forecast.copy()




    # ===============================
    # SAFETY CHECK
    # ===============================


    if forecast.empty:


        return """

        No forecast data available.

        """





    # ===============================
    # FORECAST VALUES
    # ===============================


    latest_prediction = (

        forecast["yhat"]

        .iloc[-1]

    )




    first_prediction = (

        forecast["yhat"]

        .iloc[0]

    )




    highest_prediction = (

        forecast["yhat"]

        .max()

    )




    lowest_prediction = (

        forecast["yhat"]

        .min()

    )




    average_prediction = (

        forecast["yhat"]

        .mean()

    )






    growth = (


        (

            latest_prediction

            -

            first_prediction

        )

        /

        max(

            first_prediction,

            1

        )

        *

        100

    )









    # ===============================
    # AI KNOWLEDGE
    # ===============================


    context=f"""

You are AURA Forecast Intelligence AI.


ROLE:

- Senior Revenue Forecast Analyst
- Restaurant Business Consultant
- Financial Intelligence Expert



You analyze Prophet Machine Learning forecasts.



Revenue Type:

NET REVENUE


Formula:

Net Revenue =
Total Billing
- GST
- Discounts
+ Service Charges
+ Delivery Charges





====================
FORECAST SUMMARY
====================


Starting Forecast:

₹{first_prediction:,.2f}



Final Forecast:

₹{latest_prediction:,.2f}



Highest Expected Revenue:

₹{highest_prediction:,.2f}



Lowest Expected Revenue:

₹{lowest_prediction:,.2f}



Average Expected Revenue:

₹{average_prediction:,.2f}



Expected Growth Trend:

{growth:.2f}%





RULES:

1. Explain revenue direction.

2. Explain possible restaurant reasons.

3. Suggest practical actions.

4. Focus on profit improvement.

5. Never invent numbers.

6. Only use provided forecast values.



"""


    return context







# ==================================
# ASK FORECAST AI
# ==================================

def explain_forecast_ai(
        question,
        forecast
):


    try:


        context = prepare_forecast_context(

            forecast

        )




        response = ollama.chat(


            model="phi3:mini",



            messages=[


                {

                    "role":"system",

                    "content":context

                },



                {

                    "role":"user",

                    "content":question

                }


            ],



            options={


                "temperature":0.2,


                "num_ctx":2048,


                "num_predict":300,


                "top_p":0.8


            }


        )






        return (

            response["message"]["content"]

        )






    except Exception as e:


        return f"""

⚠️ AURA Forecast AI unavailable.


Forecast engine is working.


Issue:
{e}



Fix:

1. Open CMD

2. Run:

ollama serve


3. Check model:

ollama list


"""