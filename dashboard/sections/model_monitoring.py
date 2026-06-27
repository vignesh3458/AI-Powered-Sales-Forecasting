import streamlit as st

import plotly.express as px

import pandas as pd


from components.chart_theme import (
    apply_chart_theme
)


from forecasting.xgboost_model import (
    evaluate_xgboost
)



# ================================
# CACHE
# ================================


@st.cache_data(
    ttl=86400,
    show_spinner=False
)


def cached_metrics(df):


    return evaluate_xgboost(df)





def show_model_monitoring(df):


    st.title(
        "AI Forecast Model Monitoring"
    )



    with st.spinner(
        "Evaluating AI Forecast Engine..."
    ):


        metrics = cached_metrics(
            df
        )



    # ================================
    # KPI SECTION
    # ================================


    st.subheader(
        "🎯 Forecast Accuracy"
    )


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "Accuracy",

        f"{metrics['Accuracy']}%"

    )


    c2.metric(

        "MAPE",

        f"{metrics['MAPE']}%"

    )


    c3.metric(

        "RMSE",

        f"₹{metrics['RMSE']:,.0f}"

    )


    c4.metric(

        "MAE",

        f"₹{metrics['MAE']:,.0f}"

    )




    # ================================
    # BUSINESS HEALTH
    # ================================


    st.subheader(
        "📈 Business Health"
    )


    b1,b2,b3 = st.columns(3)



    b1.metric(

        "Revenue Growth",

        f"{metrics['Growth']}%"

    )



    b2.metric(

        "AI Model Score",

        f"{metrics['Score']}/100"

    )



    if metrics["Score"] >= 90:


        grade="A+"


    elif metrics["Score"] >= 80:


        grade="A"


    elif metrics["Score"] >=70:


        grade="B"


    else:


        grade="C"



    b3.metric(

        "Model Grade",

        grade

    )




    # ================================
    # STATUS MESSAGE
    # ================================


    if metrics["Score"] >=85:


        st.success(

            "🏆 Excellent AI Forecast Model"

        )


    elif metrics["Score"] >=70:


        st.info(

            "✅ Stable Forecast Performance"

        )


    else:


        st.warning(

            "⚠️ Model requires improvement"

        )





    # ================================
    # ACTUAL VS PREDICTED
    # ================================


    st.subheader(

        "📊 Actual vs Predicted Revenue"

    )



    if (

        len(metrics["Actual"]) > 0

        and

        len(metrics["Predicted"]) > 0

    ):


        compare = pd.DataFrame(

            {

                "Actual Revenue":

                    metrics["Actual"],


                "AI Prediction":

                    metrics["Predicted"]

            }

        )



        fig = px.line(

            compare,

            y=[

                "Actual Revenue",

                "AI Prediction"

            ],

            markers=True,

            title="AI Backtesting Performance"

        )


        fig = apply_chart_theme(

            fig

        )



        st.plotly_chart(

            fig,

            width="stretch",

            key="actual_prediction"

        )





    # ================================
    # ERROR ANALYSIS
    # ================================


    st.subheader(

        "📉 Forecast Error Analysis"

    )


    error_df = pd.DataFrame(

        {

            "Metric":[

                "MAPE",

                "MAE",

                "RMSE"

            ],


            "Value":[

                metrics["MAPE"],

                metrics["MAE"],

                metrics["RMSE"]

            ]

        }

    )



    fig2 = px.bar(

        error_df,

        x="Metric",

        y="Value",

        text_auto=True,

        title="Model Error Metrics"

    )


    fig2 = apply_chart_theme(

        fig2

    )


    st.plotly_chart(

        fig2,

        width="stretch",

        key="error_chart"

    )


    # ================================
    # AI RECOMMENDATION
    # ================================


    st.subheader(

        "💡 AI Recommendation"

    )



    if metrics["MAPE"] <= 15:


        st.success(

            """

            🚀 Forecast engine performance is excellent.


            Suitable for:


            ✔ Revenue Forecasting


            ✔ Stock Planning


            ✔ Business Decisions


            ✔ Growth Analysis

            """

        )


    elif metrics["MAPE"] <=25:


        st.info(

            """

            Forecast quality is good.


            More seasonal history can improve accuracy.

            """

        )



    else:


        st.warning(

            """

            Improve model by:


            - Adding more historical data


            - Removing abnormal sales events


            - Adding external features

            """

        )