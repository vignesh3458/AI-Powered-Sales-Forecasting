
import streamlit as st

import plotly.express as px

import pandas as pd

from io import BytesIO

from forecasting.forecast_insights import (
    generate_forecast_insight
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table
)


from reportlab.lib.styles import (
    getSampleStyleSheet
)

from forecasting.forecast_model import generate_forecast

def create_forecast_pdf(
        df,
        forecast_display
):


    buffer = BytesIO()


    pdf = SimpleDocTemplate(
        buffer
    )


    styles = getSampleStyleSheet()


    content = []


    # -----------------------
    # TITLE
    # -----------------------

    content.append(

        Paragraph(

            "AI SALES FORECAST REPORT",

            styles["Title"]

        )

    )


    content.append(
        Spacer(1,20)
    )



    # -----------------------
    # KPI SUMMARY
    # -----------------------


    content.append(

        Paragraph(

            "Executive KPI Summary",

            styles["Heading2"]

        )

    )



    kpi_table = [

        [
            "Metric",
            "Value"
        ],


        [
            "Total Revenue",

            f"₹{df['Net_Revenue'].sum():,.2f}"

        ],


        [
            "Transactions",

            len(df)

        ],


        [
            "Average Bill",

            f"₹{df['Net_Revenue'].mean():,.2f}"

        ],


        [
            "Items Sold",

            int(
                df["Quantity"].sum()
            )

        ]

    ]


    table = Table(
        kpi_table
    )


    content.append(
        table
    )


    content.append(
        Spacer(1,20)
    )


    # -----------------------
    # FORECAST SUMMARY
    # -----------------------


    content.append(

        Paragraph(

            "Forecast Summary",

            styles["Heading2"]

        )

    )


    forecast_text = f"""

    Average Forecast Revenue:
    ₹{forecast_display['Predicted Revenue'].mean():,.2f}


    Highest Forecast Revenue:
    ₹{forecast_display['Predicted Revenue'].max():,.2f}

    """


    content.append(

        Paragraph(

            forecast_text,

            styles["Normal"]

        )

    )


    content.append(
        Spacer(1,20)
    )


    # -----------------------
    # BUSINESS INSIGHTS
    # -----------------------


    best_category = (

        df.groupby("Category")
        ["Net_Revenue"]
        .sum()
        .idxmax()

    )


    best_meal = (

        df.groupby("Meal_Period")
        ["Net_Revenue"]
        .sum()
        .idxmax()

    )


    best_payment = (

        df.groupby("Payment_Method")
        ["Net_Revenue"]
        .sum()
        .idxmax()

    )



    insight_text=f"""


    Best Category: {best_category}


    Best Meal Period: {best_meal}


    Best Payment Method: {best_payment}



    AI Recommendation:


    Focus inventory and marketing efforts on {best_category}
    during {best_meal} period.

    """



    content.append(

        Paragraph(

            "AI Business Insights",

            styles["Heading2"]

        )

    )


    content.append(

        Paragraph(

            insight_text,

            styles["Normal"]

        )

    )


    pdf.build(
        content
    )


    buffer.seek(0)


    return buffer
    
    
def create_forecast_excel(
        df,
        forecast_display
):


    output = BytesIO()


    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:


        # ======================
        # KPI SUMMARY
        # ======================

        summary = pd.DataFrame(
            {

            "Metric":[

                "Total Revenue",
                "Transactions",
                "Average Bill",
                "Total Items Sold",
                "Average Forecast",
                "Highest Forecast"

            ],


            "Value":[

                df["Net_Revenue"].sum(),

                len(df),

                df["Net_Revenue"].mean(),

                df["Quantity"].sum(),

                forecast_display[
                    "Predicted Revenue"
                ].mean(),

                forecast_display[
                    "Predicted Revenue"
                ].max()

            ]

            }
        )


        summary.to_excel(

            writer,

            sheet_name="Executive Summary",

            index=False

        )


        # ======================
        # FORECAST
        # ======================


        forecast_display.to_excel(

            writer,

            sheet_name="Forecast Data",

            index=False

        )


        # ======================
        # CATEGORY
        # ======================


        revenue_col = (
            "Net_Revenue"
            if "Net_Revenue" in df.columns
            else "Total_Billed"
        )


        category = (

            df.groupby("Category")
            [revenue_col]
            .sum()
            .reset_index()

        )


        category.to_excel(

            writer,

            sheet_name="Category Analysis",

            index=False

        )


        # ======================
        # PRODUCTS
        # ======================


        products = (

            df.groupby("Item_Name")
            ["Quantity"]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()

        )


        products.to_excel(

            writer,

            sheet_name="Products",

            index=False

        )


        # ======================
        # INSIGHTS
        # ======================


        insights = pd.DataFrame(

            {

            "Insight":[

                "Best Category",

                "Best Meal Period",

                "Best Payment Method"

            ],


            "Result":[


                df.groupby("Category")
                [revenue_col]
                .sum()
                .idxmax(),


                df.groupby("Meal_Period")
                [revenue_col]
                .sum()
                .idxmax(),


                df.groupby("Payment_Method")
                [revenue_col]
                .sum()
                .idxmax()

            ]

            }

        )


        insights.to_excel(

            writer,

            sheet_name="AI Insights",

            index=False

        )


    return output.getvalue()
    

@st.cache_data(
    ttl=86400,
    show_spinner=False
)


def cached_forecast(

        df,

        days,

        category

):


    return generate_forecast(

        df,

        periods=days,

        category=category

    )
def show_forecast(df):


    st.subheader(
        " AI Revenue Forecast"
    )



    # =====================
    # SIDEBAR OPTIONS
    # =====================


    days = st.slider(

        "Forecast Days",

        7,

        90,

        30

    )





    if "Category" in df.columns:


        categories = (

            ["All"]

            +

            sorted(

                df["Category"]

                .astype(str)

                .unique()

                .tolist()

            )

        )


    else:


        categories=[

            "All"

        ]





    selected_category = st.selectbox(

        "Category Forecast",

        categories

    )






    # =====================
    # GENERATE FORECAST
    # =====================


    with st.spinner(

        "Training Forecast Model..."

    ):


        forecast = cached_forecast(

            df,

            days,

            selected_category

        )








    # =====================
    # ONLY FUTURE DATA
    # =====================


    last_date = pd.to_datetime(

        df["Date"]

    ).max()




    future_forecast = (

        forecast[

            forecast["ds"]

            >

            last_date

        ]

    )







    # =====================
    # KPI
    # =====================


    total_prediction = (

        future_forecast["yhat"]

        .sum()

    )



    avg_prediction = (

        future_forecast["yhat"]

        .mean()

    )






    c1,c2 = st.columns(2)



    c1.metric(

        "Predicted Revenue",

        f"₹{total_prediction:,.0f}"

    )




    c2.metric(

        "Average Daily Revenue",

        f"₹{avg_prediction:,.0f}"

    )









    # =====================
    # FORECAST CHART
    # =====================


    st.subheader(

        "📈 Revenue Prediction Trend"

    )



    fig = px.line(

        future_forecast,


        x="ds",


        y="yhat",


        markers=True,


        title="Future Net Revenue Forecast"

    )





    fig.update_layout(

        height=500,

        hovermode="x unified"

    )





    st.plotly_chart(

        fig,

        width="stretch"

    )

    # ==========================
    # AI FORECAST INSIGHT
    # ==========================


    st.subheader(
        "💡 AI Forecast Insights"
    )



    insight = generate_forecast_insight(

        future_forecast,

        df

    )



    c1,c2 = st.columns(2)



    c1.metric(

        "Forecast Trend",

        insight["Trend"]

    )


    c2.metric(

        "Expected Change",

        f"{insight['Change']}%"

    )




    st.info(

        insight["Message"]

    )



    st.write(

        "Recommended Actions"

    )



    for action in insight["Actions"]:


        st.success(

            "✔ " + action

        )






    # =====================
    # CONFIDENCE RANGE
    # =====================

    st.subheader(

        "📊 Forecast Confidence"

    )



    confidence = future_forecast[

        [

            "ds",

            "yhat_lower",

            "yhat",

            "yhat_upper"

        ]

    ].copy()



    # ==============================
    # RENAME DISPLAY COLUMNS
    # ==============================


    confidence = confidence.rename(

        columns={

            "ds":

                "Date",


            "yhat_lower":

                "Lower",


            "yhat":

                "Predicted Revenue",


            "yhat_upper":

                "Upper"

        }

    )




    st.dataframe(

        confidence,

        use_container_width=True

    )



    # ==============================
    # DOWNLOAD DATA
    # ==============================


    forecast_display = future_forecast.rename(

        columns={

            "ds":

                "Date",


            "yhat_lower":

                "Lower",


            "yhat":

                "Predicted Revenue",


            "yhat_upper":

                "Upper"

        }

    )



    c1,c2 = st.columns(2)



    with c1:


        st.download_button(

            "📄 Download PDF",

            create_forecast_pdf(

                df,

                forecast_display

            ),

            "forecast_report.pdf"

        )



    with c2:


        st.download_button(

            "📊 Download Excel",

            create_forecast_excel(

                df,

                forecast_display

            ),

            "forecast_report.xlsx"

        )


    # =====================
    # INSIGHTS
    # =====================


    if future_forecast.empty:

        st.warning(
            "Not enough data for forecasting"
        )

        return


    best_day = (

        future_forecast
        .sort_values(
            "yhat",
            ascending=False
        )
        .iloc[0]

    )





    st.success(

        f"""

        🚀 Forecast Insight


        Highest Expected Sales:


        Date:
        {best_day['ds'].date()}


        Revenue:
        ₹{best_day['yhat']:,.0f}

        """

    )