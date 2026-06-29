import ollama

import streamlit as st





# ==================================
# BUSINESS CONTEXT CACHE
# ==================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)


def prepare_business_context(df):


    df = df.copy()





    # ===============================
    # SAFETY
    # ===============================


    if "Net_Revenue" not in df.columns:


        raise ValueError(

            "Net_Revenue column missing"

        )







    # ===============================
    # CORE METRICS
    # ===============================


    total_revenue = (

        df["Net_Revenue"]
        .sum()

    )



    transactions = (

        len(df)

    )



    total_items = (

        df["Quantity"]
        .sum()

        if "Quantity" in df.columns

        else 0

    )



    avg_bill = (

        df["Net_Revenue"]
        .mean()

    )







    # ===============================
    # BUSINESS INSIGHTS
    # ===============================


    best_category = (

        df.groupby("Category")
        ["Net_Revenue"]
        .sum()
        .idxmax()

        if "Category" in df.columns

        else "Unavailable"

    )




    weak_category = (

        df.groupby("Category")
        ["Net_Revenue"]
        .sum()
        .idxmin()

        if "Category" in df.columns

        else "Unavailable"

    )





    best_item = (

        df.groupby("Item_Name")
        ["Quantity"]
        .sum()
        .idxmax()

        if "Item_Name" in df.columns

        else "Unavailable"

    )






    best_meal = (

        df.groupby("Meal_Period")
        ["Net_Revenue"]
        .sum()
        .idxmax()

        if "Meal_Period" in df.columns

        else "Unavailable"

    )







    payment = (

        df.groupby("Payment_Method")
        ["Net_Revenue"]
        .sum()
        .idxmax()

        if "Payment_Method" in df.columns

        else "Unavailable"

    )







    # ===============================
    # EXTRA INTELLIGENCE
    # ===============================


    extra_context = ""




    if "Day_Name" in df.columns:


        day = (

            df.groupby("Day_Name")
            ["Net_Revenue"]
            .sum()
            .idxmax()

        )


        extra_context += f"""

Best Revenue Day:
{day}

"""






    if "YearMonth" in df.columns:


        monthly = (

            df.groupby("YearMonth")
            ["Net_Revenue"]
            .sum()

        )


        extra_context += f"""

Best Month:
{monthly.idxmax()}

Lowest Month:
{monthly.idxmin()}

"""









    # ===============================
    # FINAL PROMPT
    # ===============================


    context=f"""

You are AURA AI.

You are an advanced restaurant
business intelligence assistant.


You understand:

- Revenue analytics
- Sales forecasting
- Customer behaviour
- Menu performance
- Growth strategy



RULES:

1. Use only given data.

2. Never create fake numbers.

3. Keep answers executive style.

4. Give practical restaurant actions.





====================
BUSINESS SUMMARY
====================


Net Revenue:
₹{total_revenue:,.2f}


Transactions:
{transactions}


Items Sold:
{total_items}


Average Bill:
₹{avg_bill:,.2f}





====================
CATEGORY
====================

Best Category:
{best_category}


Weak Category:
{weak_category}





====================
PRODUCT
====================


Top Item:

{best_item}





====================
CUSTOMERS
====================


Peak Meal:

{best_meal}


Preferred Payment:

{payment}





====================
MORE INSIGHTS
====================


{extra_context}



"""


    return context







# ==================================
# ASK AURA
# ==================================

def ask_lucid_ai(
        question,
        df
):


    try:


        context = prepare_business_context(

            df

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

⚠️ AURA AI unavailable.

Reason:
{e}


Check:
1. Ollama running

2. Run command:

ollama serve

3. Check phi3 model installed


"""