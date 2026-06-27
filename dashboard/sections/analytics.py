import streamlit as st

import plotly.express as px

import pandas as pd



from components.chart_theme import (

    apply_chart_theme,

    POWERBI_COLORS

)



# ==================================
# PREPARE ANALYTICS DATA CACHE
# ==================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)


def prepare_analytics(df):



    analytics = {}

    # ==========================
    # REVENUE COLUMN STANDARD
    # ==========================

    revenue_col = (

        "Net_Revenue"

        if "Net_Revenue" in df.columns

        else "Total_Billed"

    )


    analytics["revenue_col"] = revenue_col

    # ==========================
    # FIX DATATYPES SAFELY
    # ==========================


    text_cols = [

        "Category",

        "Meal_Period",

        "Item_Name",

        "Payment_Method",

        "Weather",

        "Day_Name",

        "Month_Name"

    ]


    for col in text_cols:


        if col in df.columns:


            df[col] = (

                df[col]

                .astype(str)

            )





    # ==========================
    # CATEGORY SALES
    # ==========================


    if (
        "Category" in df.columns
        and
        revenue_col in df.columns
    ):


        category_sales = (

            df.groupby(
                "Category",
                observed=True
            )

            [revenue_col]

            .sum()

            .reset_index()

        )



        analytics["category_sales"] = category_sales



        analytics["best_category"] = (

            category_sales

            .nlargest(
                        1,
                        revenue_col
                    )

            .iloc[0]["Category"]

        )





    # ==========================
    # MEAL SALES
    # ==========================


    if "Meal_Period" in df.columns:


        meal_sales = (

                df.groupby(
                    "Meal_Period",
                    observed=True
                )

                [revenue_col]

                .sum()

                .reset_index()

            )



        analytics["meal_sales"] = meal_sales



        analytics["best_meal"] = (

            meal_sales

            .nlargest(

                1,

                revenue_col

            )

            .iloc[0]["Meal_Period"]

        )





    # ==========================
    # MONTH / NET REVENUE GROWTH
    # ==========================


    if (

        "YearMonth" in df.columns

        and

        revenue_col in df.columns

    ):



        monthly = (

                        df.groupby("YearMonth")

                        .agg(

                            Net_Revenue=(
                                revenue_col,
                                "sum"
                            )

                        )

                        .reset_index()

                    )







        monthly["Growth_Percentage"] = (

            monthly["Net_Revenue"]

            .pct_change()

            .fillna(0)

            *

            100

        )








        monthly["Growth_Percentage"] = (

            monthly["Growth_Percentage"]

            .round(2)

        )







        analytics["monthly_sales"] = monthly


        analytics["monthly_growth"] = monthly.copy()




    # ==========================
    # WEEKEND ANALYSIS
    # ==========================


    if "Is_Weekend" in df.columns:


        weekend = (

            df.groupby(

                "Is_Weekend",

                observed=True

            )

            [revenue_col]
            .sum()

            .reset_index()

        )



        weekend["Is_Weekend"] = (

            weekend["Is_Weekend"]

            .replace(

                {

                    0:"Weekday",

                    1:"Weekend"

                }

            )

        )



        analytics["week_analysis"] = weekend





    # ==========================
    # TOP ITEMS
    # ==========================


    if "Item_Name" in df.columns:


        analytics["top_items"] = (

            df.groupby(

                "Item_Name",

                observed=True

            )

            ["Quantity"]

            .sum()

            .nlargest(10)

            .reset_index()

        )





    # ==========================
    # PAYMENT
    # ==========================


    if "Payment_Method" in df.columns:


        payment = (

            df.groupby(

                "Payment_Method",

                observed=True

            )

            [revenue_col]
            .sum()

            .reset_index()

        )



        analytics["payment_sales"] = payment



        analytics["best_payment"] = (

            payment

            .nlargest(

                1,

                revenue_col

            )

            .iloc[0]["Payment_Method"]

        )





    # ==========================
    # WEATHER
    # ==========================


    if "Weather" in df.columns:


        weather = (

            df.groupby(

                "Weather",

                observed=True

            )

            [revenue_col]

            .sum()

            .reset_index()

        )



        analytics["weather_sales"] = weather



        analytics["best_weather"] = (

            weather

            .nlargest(

                1,

                revenue_col

            )

            .iloc[0]["Weather"]

        )





    # ==========================
    # DAY SALES
    # ==========================


    if "Day_Name" in df.columns:


        analytics["day_sales"] = (

            df.groupby(

                "Day_Name",

                observed=True

            )

            [revenue_col]

            .sum()

            .reset_index()

        )





    # ==========================
    # ACTIVITY HEATMAP
    # ==========================


    if (

        "Day_Name" in df.columns

        and

        "Meal_Period" in df.columns

    ):


        analytics["activity_heatmap"] = (

            df.groupby(

                [

                    "Day_Name",

                    "Meal_Period"

                ],

                observed=True

            )

            [revenue_col]

            .sum()

            .reset_index()

        )





    # ==========================
    # DAILY HEATMAP
    # ==========================


    if "Date" in df.columns:


        daily = (

            df.groupby(

                "Date"

            )

            [revenue_col]

            .sum()

            .reset_index()

        )


        daily["Month"] = daily["Date"].dt.month

        daily["Day"] = daily["Date"].dt.day

        daily["Month_Name"] = daily["Date"].dt.month_name()

        daily["Day_of_Week"] = daily["Date"].dt.day_name()


        analytics["daily_heatmap"] = daily





    # ==========================
    # GST
    # ==========================


    if (

        "CGST" in df.columns

        and

        "SGST" in df.columns

    ):


        analytics["gst_data"] = (

            df.groupby("YearMonth")

            .agg(

                {

                    "CGST":"sum",

                    "SGST":"sum"

                }

            )

            .reset_index()

        )





    # ==========================
    # SERVICE
    # ==========================


    if "Service_Charge" in df.columns:


        analytics["service_data"] = pd.DataFrame(

            {

                "Type":[

                    "Service",

                    "Revenue"

                ],


                "Amount":[

                    df["Service_Charge"].sum(),

                    df[revenue_col].sum()

                ]

            }

        )





    # ==========================
    # DELIVERY
    # ==========================


    if "Delivery_Charge" in df.columns:


        analytics["delivery_data"] = (

            df.groupby(

                "YearMonth"

            )

            ["Delivery_Charge"]

            .sum()

            .reset_index()

        )



    return analytics





# ==================================
# POWER BI BAR CHART
# ==================================

def create_bar_chart(
        data,
        x,
        y,
        title,
        orientation="v"
):


    fig = px.bar(

        data,

        x=x,

        y=y,

        orientation=orientation,

        color=y if orientation=="v" else x,

        text_auto=True,

        title=title,

        color_continuous_scale="Turbo"

    )


    fig.update_traces(

        textposition="outside",

        hovertemplate=

        "<b>%{label}</b><br>"
        +
        "Value: %{value}<extra></extra>"

    )


    fig.update_layout(

        height=480,

        showlegend=False

    )


    return apply_chart_theme(fig)






# ==================================
# POWER BI RANKING BAR
# ==================================

def create_ranking_chart(
        data,
        x,
        y,
        title
):


    fig = px.bar(

        data,

        x=x,

        y=y,

        orientation="h",

        color=x,

        text_auto=True,

        title=title,

        color_continuous_scale="Plasma"

    )


    fig.update_layout(

        height=550,

        showlegend=False

    )


    fig.update_yaxes(

        autorange="reversed"

    )


    return apply_chart_theme(fig)








# ==================================
# POWER BI TREEMAP
# ==================================

def create_treemap(

        data,

        path,

        values,

        title

):


    fig = px.treemap(

        data,

        path=path,

        values=values,

        color=values,

        color_continuous_scale="Turbo",

        title=title

    )


    fig.update_traces(

        textinfo="label+value+percent root"

    )


    fig.update_layout(

        height=500,

        coloraxis_showscale=False

    )


    return apply_chart_theme(fig)








# ==================================
# POWER BI BUBBLE
# ==================================

def create_bubble(

        data,

        x,

        y,

        size,

        title

):


    fig = px.scatter(

        data,

        x=x,

        y=y,

        size=size,

        color=size,

        color_continuous_scale="Rainbow",

        title=title,

        size_max=60

    )


    fig.update_layout(

        height=500

    )


    return apply_chart_theme(fig)








# ==================================
# POWER BI DONUT
# ==================================

def create_pie_chart(

        data,

        names,

        values,

        title

):


    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=0.65,

        title=title,

        color_discrete_sequence=POWERBI_COLORS

    )


    fig.update_traces(

        textinfo="percent+label",

        textposition="inside"

    )


    fig.update_layout(

        height=450

    )


    return apply_chart_theme(fig)

def show_analytics(df):


    # =============================
    # EMPTY DATA PROTECTION
    # =============================


    if df.empty:


        st.warning(

            "No data available for selected filters"

        )


        return






    analytics = prepare_analytics(

        df

    )

    revenue_col = analytics["revenue_col"]



    st.subheader(

        "Sales Intelligence Dashboard"

    )






    overview_tab, trend_tab, advanced_tab = st.tabs(

        [

            "📊 Overview",

            "📈 Trends",

            "⚙ Advanced"

        ]

    )

    # ==============================
    # OVERVIEW TAB
    # ==============================


    with overview_tab:


        # =============================
        # CATEGORY REVENUE HORIZONTAL BAR
        # =============================


        if "category_sales" in analytics:


            category_sales = (

                analytics["category_sales"]

                .sort_values(

                    revenue_col,

                    ascending=True

                )

                .copy()

            )



            fig_category = px.bar(

                category_sales,

                x= revenue_col,

                y="Category",

                orientation="h",

                title="Revenue by Category",

                color=revenue_col,

                color_continuous_scale="Turbo",

                text_auto=True

            )




            fig_category.update_traces(

                texttemplate="₹%{x:,.0f}",

                textposition="outside",


                hovertemplate=

                "<b>%{y}</b><br>"
                +
                "Revenue : ₹%{x:,.0f}"

            )




            fig_category.update_layout(

                height=520,


                xaxis_title="Revenue",


                yaxis_title="",


                showlegend=False,


                coloraxis_showscale=False,


                bargap=0.35

            )




            fig_category = apply_chart_theme(

                fig_category

            )





            st.plotly_chart(

                fig_category,

                width="stretch",

                key="powerbi_category_bar"

            )






        # =============================
        # MEAL PERIOD DONUT CHART
        # =============================


        if "meal_sales" in analytics:


            meal_sales = (

                analytics["meal_sales"]

                .copy()

            )





            fig_meal = px.pie(

                meal_sales,


                names="Meal_Period",


                values=revenue_col,


                hole=0.65,


                title="Meal Period Revenue Share",


                color_discrete_sequence=[


                    "#00C2FF",


                    "#FFB000",


                    "#FF1F3D",


                    "#7C3AED"


                ]

            )





            fig_meal.update_traces(


                textposition="inside",


                textinfo="percent+label",


                pull=[

                    0.05

                    for _ in range(

                        len(meal_sales)

                    )

                ],


                hovertemplate=

                "<b>%{label}</b><br>"
                +
                "Revenue : ₹%{value:,.0f}<br>"
                +
                "Share : %{percent}"

            )





            fig_meal.update_layout(


                height=450,


                showlegend=True


            )





            fig_meal = apply_chart_theme(

                fig_meal

            )





            st.plotly_chart(

                fig_meal,

                width="stretch",

                key="powerbi_meal_donut"

            )








        # =============================
        # BEST DAY INSIGHT
        # =============================


        if "day_sales" in analytics:


            day_sales = (

                analytics["day_sales"]

                .copy()

            )



            best_day = (

                day_sales

                .sort_values(

                    revenue_col,

                    ascending=False

                )

                .iloc[0]

                ["Day_Name"]

            )




            best_revenue = (

                day_sales

                [revenue_col]

                .max()

            )





            st.success(

                f"Highest Revenue Day: {best_day} (₹{best_revenue:,.2f})"

            )






    # ==============================
    # TREND TAB
    # ==============================


    with trend_tab:



        if "monthly_sales" in analytics:



            monthly_sales = (

                analytics["monthly_sales"]

                .copy()

            )



            # =============================
            # MOVING AVERAGE TREND
            # =============================


            monthly_sales["Moving_Avg"] = (

                monthly_sales["Net_Revenue"]

                .rolling(

                    window=3,

                    min_periods=1

                )

                .mean()

            )






            # =============================
            # POWER BI ADVANCED LINE CHART
            # =============================


            fig_month = px.line(


            monthly_sales,


            x="YearMonth",


            y=[

                "Net_Revenue",

                "Moving_Avg"

            ],


            markers=True,


            title="AI Net Revenue Trend Intelligence"


        )






            fig_month.update_traces(


                line=dict(

                    width=5,

                    shape="spline"

                ),



                marker=dict(

                    size=10

                ),



                hovertemplate=

                "<b>Month:</b> %{x}<br>"

                +

                "Revenue: ₹%{y:,.0f}"

            )








            # =============================
            # HIGHLIGHT LATEST MONTH
            # =============================


            latest_month = (

                monthly_sales

                .iloc[-1]

            )




            fig_month.add_annotation(


                x=latest_month["YearMonth"],


                y=latest_month["Net_Revenue"],


                text=

                f"Latest<br>₹{latest_month['Net_Revenue']:,.0f}",



                showarrow=True,


                arrowhead=3


            )









            # =============================
            # HIGHEST REVENUE POINT
            # =============================


            best_month = (

                monthly_sales.loc[

                    monthly_sales["Net_Revenue"]

                    .idxmax()

                ]

            )





            fig_month.add_annotation(


                x=best_month["YearMonth"],


                y=best_month["Net_Revenue"],


                text="🏆 Peak",


                showarrow=True,


                arrowhead=2

            )









            # =============================
            # POWER BI LAYOUT
            # =============================


            fig_month.update_layout(


                height=550,


                hovermode="x unified",


                legend_title="",


                xaxis=dict(


                    title="",


                    rangeslider=dict(


                        visible=True


                    )

                ),



                yaxis=dict(


                    title="Revenue"


                )

            )








            fig_month = apply_chart_theme(


                fig_month


            )







            st.plotly_chart(


                fig_month,


                width="stretch",


                key="advanced_revenue_line_chart"


            )








        latest_revenue = monthly_sales["Net_Revenue"].iloc[-1]


        if len(monthly_sales) > 1:

            previous_revenue = monthly_sales["Net_Revenue"].iloc[-2]

            growth = (
                (latest_revenue - previous_revenue)
                /
                max(previous_revenue,1)
                *
                100
            )

        else:

            growth = 0



        if growth > 0:

            st.success(

                f"📈 Revenue increased by {growth:.2f}% compared to previous month"

            )


        elif growth < 0:

            st.warning(

                f"📉 Revenue decreased by {abs(growth):.2f}% compared to previous month"

            )


        else:

            st.info(

                "No monthly growth change available"

            )



    # ==============================
    # ADVANCED TAB
    # ==============================


    with advanced_tab:


        # =============================
        # POWER BI REVENUE MATRIX HEATMAP
        # =============================


        with st.expander(

            "Revenue Performance Matrix",

            expanded=False

        ):



            if "daily_heatmap" in analytics:



                heatmap_data = (

                    analytics["daily_heatmap"]

                    .copy()

                )






                # =============================
                # CREATE MATRIX
                # =============================


                heatmap_pivot = (

                    heatmap_data

                    .pivot_table(

                        index="Day_of_Week",

                        columns="Month_Name",

                        values=revenue_col,

                        aggfunc="sum",

                        fill_value=0

                    )

                )








                # =============================
                # POWER BI MATRIX VISUAL
                # =============================


                fig_heatmap = px.imshow(


                    heatmap_pivot,


                    title="Revenue Intensity Matrix",


                    color_continuous_scale="Turbo",


                    aspect="auto",


                    text_auto=".2s"


                )








                fig_heatmap.update_traces(


                    hovertemplate=

                    "<b>Day:</b> %{y}<br>"
                    +
                    "<b>Month:</b> %{x}<br>"
                    +
                    "<b>Revenue:</b> ₹%{z:,.0f}"

                    +

                    "<extra></extra>"


                )








                fig_heatmap.update_layout(


                    height=550,


                    xaxis_title="",


                    yaxis_title="",



                    coloraxis_colorbar=dict(

                        title="Revenue"

                    )

                )








                fig_heatmap = apply_chart_theme(

                    fig_heatmap

                )








                st.plotly_chart(

                    fig_heatmap,

                    width="stretch",

                    key="powerbi_revenue_matrix"

                )









                # =============================
                # PEAK PERFORMANCE INSIGHT
                # =============================


                peak_day = (

                    heatmap_data

                    .sort_values(

                        revenue_col,

                        ascending=False

                    )

                    .iloc[0]

                )









                st.success(

                    f"""

🔥 Peak Revenue Pattern


📅 Day:

{peak_day['Day_of_Week']}


🗓 Month:

{peak_day['Month_Name']}


💰 Revenue:

₹{peak_day[revenue_col]:,.0f}


"""

                )






            else:


                st.info(

                    "Revenue heatmap data unavailable"

                )
   
    # =============================
    # WEEKDAY VS WEEKEND ANALYSIS
    # =============================


    if "week_analysis" in analytics:


        st.subheader(

            "Weekday vs Weekend Revenue"

        )




        week_analysis = (

            analytics["week_analysis"]

            .copy()

        )





        # =============================
        # POWER BI DONUT CHART
        # =============================


        total_week_revenue = (

            week_analysis[revenue_col]

            .sum()

        )





        fig_week = px.pie(

            week_analysis,


            names="Is_Weekend",


            values=revenue_col,


            hole=0.68,


            title="Weekday vs Weekend Revenue Share",


            color_discrete_sequence=[

                "#118DFF",

                "#FFB000"

            ]

        )







        fig_week.update_traces(


            textposition="inside",


            textinfo="percent+label",



            pull=[

                0.04

                for _ in range(

                    len(

                        week_analysis

                    )

                )

            ],




            hovertemplate=

            "<b>%{label}</b><br>"

            +

            "Revenue : ₹%{value:,.0f}<br>"

            +

            "Contribution : %{percent}"

            +

            "<extra></extra>"

        )








        fig_week.update_layout(


            height=460,


            showlegend=True,



            annotations=[


                dict(

                    text=

                    f"Total<br>₹{total_week_revenue/100000:.1f}L",


                    x=0.5,


                    y=0.5,


                    font_size=20,


                    showarrow=False

                )

            ]

        )








        fig_week = apply_chart_theme(

            fig_week

        )








        st.plotly_chart(

            fig_week,

            width="stretch",

            key="powerbi_weekend_donut"

        )










        # =============================
        # BUSINESS INSIGHT
        # =============================


        top_period = (

            week_analysis

            .sort_values(

                revenue_col,

                ascending=False

            )

            .iloc[0]

        )






        st.success(

            f"""

🏆 Revenue Leader


{top_period['Is_Weekend']}


Generated:


₹{top_period[revenue_col]:,.0f}


"""

        )

        # =============================
    # TOP SELLING ITEMS
    # =============================


    if "top_items" in analytics:



        st.subheader(

            "🏆 Top Selling Items"

        )




        top_items = (

            analytics["top_items"]

            .sort_values(

                "Quantity",

                ascending=True

            )

            .copy()

        )




        # =============================
        # CREATE RANK LABEL
        # =============================


        top_items["Rank_Item"] = (

            "#"

            +

            (

                len(top_items)

                -

                top_items.index

            )

            .astype(str)

            +

            "  "

            +

            top_items["Item_Name"]

            .astype(str)

        )







        # =============================
        # POWER BI GRADIENT BAR
        # =============================


        fig_items = px.bar(


            top_items,


            x="Quantity",


            y="Rank_Item",


            orientation="h",


            title="Top Selling Items Leaderboard",



            color="Quantity",



            color_continuous_scale=[


                "#118DFF",


                "#00C2FF",


                "#7C3AED",


                "#FF1F3D",


                "#FFB000"


            ],



            text_auto=True

        )









        fig_items.update_traces(


            texttemplate="%{x:,.0f}",


            textposition="outside",




            hovertemplate=

            "<b>%{y}</b><br>"

            +

            "Quantity Sold : %{x:,.0f}"

            +

            "<extra></extra>"

        )










        fig_items.update_layout(


            height=560,


            showlegend=False,


            coloraxis_showscale=False,


            xaxis_title="Quantity Sold",


            yaxis_title="",


            bargap=0.35

        )








        fig_items = apply_chart_theme(

            fig_items

        )








        st.plotly_chart(


            fig_items,


            width="stretch",


            key="powerbi_top_items_gradient"

        )





       # =============================
    # PAYMENT ANALYSIS
    # =============================


    if "payment_sales" in analytics:



        st.subheader(

            "Customer Payment Intelligence"

        )




        payment_sales = (

            analytics["payment_sales"]

            .sort_values(

                revenue_col,

                ascending=True

            )

            .copy()

        )





        # =============================
        # POWER BI PAYMENT BAR CHART
        # =============================


        fig_payment = px.bar(


            payment_sales,


            x=revenue_col,


            y="Payment_Method",


            orientation="h",



            title="💳 Revenue by Payment Method",



            color=revenue_col,



            color_continuous_scale=[


                "#00C2FF",


                "#118DFF",


                "#7C3AED",


                "#FF1F3D"


            ],



            text_auto=True

        )








        fig_payment.update_traces(


            texttemplate="₹%{x:,.0f}",



            textposition="outside",





            hovertemplate=

            "<b>%{y}</b><br>"

            +

            "Revenue : ₹%{x:,.0f}"

            +

            "<extra></extra>"

        )









        fig_payment.update_layout(


            height=520,


            showlegend=False,


            coloraxis_showscale=False,


            xaxis_title="Revenue",


            yaxis_title="",


            bargap=0.35

        )









        fig_payment = apply_chart_theme(

            fig_payment

        )









        st.plotly_chart(


            fig_payment,


            width="stretch",


            key="powerbi_payment_bar"

        )









        # =============================
        # PAYMENT INSIGHT
        # =============================


        best_payment = (

            payment_sales

            .sort_values(

                revenue_col,

                ascending=False

            )

            .iloc[0]

        )





        st.success(

            f"""

 Preferred Payment Mode


{best_payment['Payment_Method']}


Revenue Generated:


₹{best_payment[revenue_col]:,.0f}

"""

        )
        
        # =============================
        # POWER BI DAILY REVENUE MATRIX
        # =============================


        with st.expander(

            "📅 Daily Revenue Intelligence Matrix",

            expanded=False

        ):



            if "daily_heatmap" in analytics:



                heatmap_data = (

                    analytics["daily_heatmap"]

                    .copy()

                )







                # =============================
                # CREATE DAILY MATRIX
                # =============================


                heatmap_pivot = (

                    heatmap_data

                    .pivot_table(

                        index="Day",

                        columns="Month",

                        values=revenue_col,

                        aggfunc="sum",

                        fill_value=0

                    )

                )








                # =============================
                # POWER BI HEATMAP
                # =============================


                fig_daily_heatmap = px.imshow(


                    heatmap_pivot,


                    title="Daily Revenue Performance Matrix",


                    color_continuous_scale=[


                        "#0B1120",


                        "#118DFF",


                        "#00C2FF",


                        "#FFB000",


                        "#FF1F3D"


                    ],


                    aspect="auto",


                    text_auto=".2s"

                )









                fig_daily_heatmap.update_traces(


                    hovertemplate=

                    "<b>Day:</b> %{y}<br>"

                    +

                    "<b>Month:</b> %{x}<br>"

                    +

                    "Revenue : ₹%{z:,.0f}"

                    +

                    "<extra></extra>"


                )









                fig_daily_heatmap.update_layout(


                    height=600,


                    xaxis_title="",


                    yaxis_title="Day",



                    coloraxis_colorbar=dict(

                        title="Revenue"

                    )

                )









                fig_daily_heatmap = apply_chart_theme(

                    fig_daily_heatmap

                )










                st.plotly_chart(

                    fig_daily_heatmap,

                    width="stretch",

                    key="powerbi_daily_heatmap"

                )










                # =============================
                # DAILY AI INSIGHT
                # =============================


                peak_day = (

                    heatmap_data

                    .sort_values(

                        revenue_col,

                        ascending=False

                    )

                    .iloc[0]

                )







                st.success(

                    f"""

    🔥 Highest Revenue Date


    Day:

    {peak_day['Day']}


    Month:

    {peak_day['Month']}


    Revenue:

    ₹{peak_day[revenue_col]:,.0f}

    """

                )






            else:


                st.info(

                    "Daily revenue data unavailable"

                )

    # =============================
    # POWER BI WEEKLY PERFORMANCE RADAR
    # =============================


    if "day_sales" in analytics:


        st.subheader(

            "📅 Weekly Revenue Intelligence"

        )




        day_sales = (

            analytics["day_sales"]

            .copy()

        )





        # =============================
        # FIX DAY ORDER
        # =============================


        day_order = [

            "Monday",

            "Tuesday",

            "Wednesday",

            "Thursday",

            "Friday",

            "Saturday",

            "Sunday"

        ]




        day_sales["Day_Name"] = pd.Categorical(

            day_sales["Day_Name"],

            categories=day_order,

            ordered=True

        )




        day_sales = (

            day_sales

            .sort_values(

                "Day_Name"

            )

        )








        # =============================
        # POWER BI RADAR CHART
        # =============================


        fig_day_sales = px.line_polar(


            day_sales,


            r=revenue_col,


            theta="Day_Name",


            line_close=True,


            markers=True,


            title="Weekly Revenue Pattern"


        )









        fig_day_sales.update_traces(


            fill="toself",



            line=dict(

                width=5

            ),



            marker=dict(

                size=10

            ),



            hovertemplate=

            "<b>%{theta}</b><br>"

            +

            "Revenue : ₹%{r:,.0f}"

            +

            "<extra></extra>"

        )









        fig_day_sales.update_layout(


            height=550,


            polar=dict(


                radialaxis=dict(

                    visible=True

                )

            ),



            showlegend=False

        )










        fig_day_sales = apply_chart_theme(

            fig_day_sales

        )










        st.plotly_chart(


            fig_day_sales,


            width="stretch",


            key="powerbi_weekly_radar"


        )











        # =============================
        # WEEKLY INSIGHT
        # =============================


        best_day = (

            day_sales

            .sort_values(

                revenue_col,

                ascending=False

            )

            .iloc[0]

        )








        st.success(

            f"""

🏆 Best Performing Day


📅 {best_day['Day_Name']}


💰 Revenue:


₹{best_day[revenue_col]:,.0f}

"""

        )
   
    # =============================
    # POWER BI MONTHLY GROWTH
    # WATERFALL ANALYSIS
    # =============================


    if "monthly_growth" in analytics:


        st.subheader(

            "📈 Revenue Growth Intelligence"

        )




        monthly_growth = (

            analytics["monthly_growth"]

            .copy()

        )






        # =============================
        # CALCULATE GROWTH %
        # =============================


        monthly_growth["Growth_Percentage"] = (

            monthly_growth["Net_Revenue"]

            .pct_change()

            .fillna(0)

            *

            100

        )




        monthly_growth["Growth_Percentage"] = (

            monthly_growth["Growth_Percentage"]

            .round(2)

        )








        # =============================
        # KPI CARDS
        # =============================


        latest_growth = (

            monthly_growth

            ["Growth_Percentage"]

            .iloc[-1]

        )



        best_growth = (

            monthly_growth

            ["Growth_Percentage"]

            .max()

        )



        avg_growth = (

            monthly_growth

            ["Growth_Percentage"]

            .mean()

        )






        c1,c2,c3 = st.columns(3)




        c1.metric(

            "📈 Latest Growth",

            f"{latest_growth:.2f}%"

        )




        c2.metric(

            "🚀 Best Growth",

            f"{best_growth:.2f}%"

        )





        c3.metric(

            "📊 Avg Growth",

            f"{avg_growth:.2f}%"

        )









        # =============================
        # POWER BI WATERFALL CHART
        # =============================


        fig_growth = px.bar(


            monthly_growth,


            x="YearMonth",


            y="Growth_Percentage",


            title="Month Over Month Growth Movement",


            color="Growth_Percentage",



            color_continuous_scale=[


                "#FF1F3D",


                "#FFB000",


                "#00C853"


            ],



            text_auto=True


        )








        fig_growth.update_traces(


            texttemplate="%{y:.1f}%",


            textposition="outside",





            hovertemplate=

            "<b>Month:</b> %{x}<br>"

            +

            "Growth : %{y:.2f}%"

            +

            "<extra></extra>"

        )








        # ZERO BASELINE


        fig_growth.add_hline(


            y=0,


            line_width=2,


            line_dash="dash"


        )








        fig_growth.update_layout(


            height=520,


            showlegend=False,


            coloraxis_showscale=False,


            hovermode="x unified",


            xaxis_title="",


            yaxis_title="Growth %"

        )









        fig_growth = apply_chart_theme(

            fig_growth

        )








        st.plotly_chart(


            fig_growth,


            width="stretch",


            key="powerbi_growth_waterfall"


        )









        # =============================
        # GROWTH INSIGHT
        # =============================


        if latest_growth > 0:


            st.success(

                f"🚀 Latest month improved by {latest_growth:.2f}%"

            )


        elif latest_growth < 0:


            st.warning(

                f"📉 Latest month dropped by {abs(latest_growth):.2f}%"

            )


        else:


            st.info(

                "Revenue remained stable this month"

            )
          # =============================
        # GROWTH AUTO INSIGHT
        # =============================


        best_month = (

            monthly_growth

            .sort_values(

                "Growth_Percentage",

                ascending=False

            )

            .iloc[0]

        )




        st.success(

            f"""

🚀 Growth Insight


Best Growth Month:

{best_month['YearMonth']}


Growth:

{best_month['Growth_Percentage']:.2f}%

"""

        )









    # =============================
    # POWER BI CATEGORY PERFORMANCE
    # =============================


    if "category_sales" in analytics:


        st.subheader(

            "🏅 Category Performance Intelligence"

        )





        category_ranking = (

            analytics["category_sales"]

            .sort_values(

                revenue_col,

                ascending=False

            )

            .copy()

        )





        category_ranking["Category"] = (

            category_ranking["Category"]

            .astype(str)

        )








        # =============================
        # POWER BI CATEGORY BAR CHART
        # =============================


        fig_category_rank = px.bar(


            category_ranking

            .sort_values(

                revenue_col,

                ascending=False

            ),



            x="Category",



            y=revenue_col,



            color=revenue_col,



            text_auto=True,



            title="Category Revenue Performance",



            color_continuous_scale=[


                "#00C2FF",


                "#118DFF",


                "#7C3AED",


                "#FF1F3D",


                "#FFB000"


            ]

        )











        fig_category_rank.update_traces(


            texttemplate="₹%{y:,.0f}",


            textposition="outside",





            marker=dict(

                line=dict(

                    width=0

                )

            ),





            hovertemplate=

            "<b>%{x}</b><br>"

            +

            "Revenue : ₹%{y:,.0f}"

            +

            "<extra></extra>"

        )









        fig_category_rank.update_layout(


            height=550,


            showlegend=False,


            coloraxis_showscale=False,


            xaxis_title="Category",


            yaxis_title="Revenue",


            bargap=0.35

        )










        fig_category_rank = apply_chart_theme(

            fig_category_rank

        )










        st.plotly_chart(


            fig_category_rank,


            width="stretch",


            key="powerbi_category_bar_rank"


        )









        # =============================
        # CATEGORY KPI INSIGHT
        # =============================


        best_category = (

            category_ranking

            .sort_values(

                revenue_col,

                ascending=False

            )

            .iloc[0]

        )








        st.success(

            f"""

🏆 Leading Category


{best_category['Category']}


Revenue Generated:


₹{best_category[revenue_col]:,.0f}

"""

        )


        # =============================
        # POWER BI MEAL PERFORMANCE
        # FUNNEL ANALYSIS
        # =============================


        if "meal_sales" in analytics:


            st.subheader(

                "🍽 Meal Period Revenue Intelligence"

            )





            meal_ranking = (

                analytics["meal_sales"]

                .sort_values(

                    revenue_col,

                    ascending=False

                )

                .copy()

            )





            meal_ranking["Meal_Period"] = (

                meal_ranking["Meal_Period"]

                .astype(str)

            )

            # =============================
            # CREATE MEAL RANK LABEL
            # =============================


            meal_ranking = (

                meal_ranking

                .sort_values(

                    revenue_col,

                    ascending=False

                )

                .reset_index(

                    drop=True

                )

                .copy()

            )



            meal_ranking["Rank"] = (

                meal_ranking.index

                +

                1

            )



            meal_ranking["Meal_Rank"] = (

                meal_ranking["Rank"]

                .astype(str)

                +

                ". "

                +

                meal_ranking["Meal_Period"]

                .astype(str)

            )







            # =============================
            # MEAL PERFORMANCE FUNNEL CHART
            # =============================


            fig_meal_rank = px.funnel(

                meal_ranking.sort_values(

                    revenue_col,

                    ascending=False

                ),


                x=revenue_col,


                y="Meal_Rank",


                color="Meal_Rank",


                title="Meal Revenue Performance Funnel",


                color_discrete_sequence=[

                    "#FF6B6B",

                    "#4ECDC4",

                    "#45B7D1",

                    "#96CEB4",

                    "#FFEAA7",

                    "#A29BFE"

                ]

            )








            fig_meal_rank.update_traces(


                texttemplate="₹%{x:,.0f}",


                textposition="inside",



                hovertemplate=

                "<b>%{y}</b><br>"
                +
                "Revenue : ₹%{x:,.0f}"

            )








            fig_meal_rank.update_layout(


                height=500,


                showlegend=False,


                xaxis_title="Revenue",


                yaxis_title=""


            )









            fig_meal_rank = apply_chart_theme(

                fig_meal_rank

            )









            st.plotly_chart(

                fig_meal_rank,

                width="stretch",

                key="powerbi_meal_funnel"

            )









            # =============================
            # WINNER INSIGHT CARD
            # =============================


            best_meal = (

                meal_ranking

                .iloc[0]

            )








            st.success(

                f"""

🏆 Meal Performance Winner


🥇 {best_meal['Meal_Period']}


💰 Revenue:


₹{best_meal[revenue_col]:,.0f}

"""

            )










            # =============================
            # TOP 3 MEDAL VIEW
            # =============================


            if len(meal_ranking) >= 3:


                st.info(

                    f"""

🏅 Meal Ranking


🥇 {meal_ranking.iloc[0]['Meal_Period']}


🥈 {meal_ranking.iloc[1]['Meal_Period']}


🥉 {meal_ranking.iloc[2]['Meal_Period']}

"""

                )
       # =============================
    # POWER BI SALES ACTIVITY MATRIX
    # =============================


    if "activity_heatmap" in analytics:


        st.subheader(

            "🔥 Sales Activity Intelligence Matrix"

        )





        heatmap_data = (

            analytics["activity_heatmap"]

            .copy()

        )






        # =============================
        # WEEKDAY ORDER FIX
        # =============================


        day_order = [

            "Monday",

            "Tuesday",

            "Wednesday",

            "Thursday",

            "Friday",

            "Saturday",

            "Sunday"

        ]





        heatmap_data["Day_Name"] = pd.Categorical(


            heatmap_data["Day_Name"],


            categories=day_order,


            ordered=True


        )








        # =============================
        # CREATE MATRIX
        # =============================


        activity_matrix = (


            heatmap_data


            .pivot_table(


                index="Day_Name",


                columns="Meal_Period",


                values=revenue_col,


                aggfunc="sum",


                fill_value=0


            )


        )










        # =============================
        # POWER BI HEATMAP
        # =============================


        fig_activity = px.imshow(



            activity_matrix,



            title="🔥 Peak Revenue Timing Intelligence",



            color_continuous_scale=[


                "#0B1120",


                "#2563EB",


                "#06B6D4",


                "#22C55E",


                "#FACC15",


                "#EF4444"


            ],



            aspect="auto",



            text_auto=".2s"


        )











        fig_activity.update_traces(


            hovertemplate=

            "<b>Day:</b> %{y}<br>"

            +

            "<b>Meal:</b> %{x}<br>"

            +

            "Revenue : ₹%{z:,.0f}"

            +

            "<extra></extra>"


        )










        fig_activity.update_layout(


            height=550,


            xaxis_title="Meal Period",


            yaxis_title="",



            coloraxis_colorbar=dict(


                title="Revenue"


            )


        )










        fig_activity = apply_chart_theme(


            fig_activity


        )










        st.plotly_chart(



            fig_activity,



            width="stretch",



            key="powerbi_activity_matrix"


        )









        # =============================
        # AUTO BUSINESS INSIGHT
        # =============================


        peak_time = (

            heatmap_data

            .sort_values(

                revenue_col,

                ascending=False

            )

            .iloc[0]

        )









        st.success(

            f"""

🔥 Peak Business Timing


📅 Day:

{peak_time['Day_Name']}


🍽 Meal:

{peak_time['Meal_Period']}


💰 Revenue:

₹{peak_time[revenue_col]:,.0f}

"""

        )






    else:


        st.info(

            "Activity heatmap unavailable"

        )


        # ===============================
        # POWER BI GST FINANCE ANALYTICS
        # ===============================


        if (

            "CGST" in df.columns

            and

            "SGST" in df.columns

        ):


            st.subheader(
                "🧾 GST Finance Intelligence"
            )


            gst_data = (

                df.groupby("YearMonth")

                [

                    [

                        "CGST",

                        "SGST"

                    ]

                ]

                .sum()

                .reset_index()

            )






            # =====================
            # KPI CARDS
            # =====================


            total_cgst = (

                gst_data["CGST"]

                .sum()

            )



            total_sgst = (

                gst_data["SGST"]

                .sum()

            )



            total_gst = (

                total_cgst

                +

                total_sgst

            )






            c1,c2,c3 = st.columns(3)




            c1.metric(

                "CGST Collected",

                f"₹{total_cgst:,.0f}"

            )




            c2.metric(

                "SGST Collected",

                f"₹{total_sgst:,.0f}"

            )




            c3.metric(

                "Total GST",

                f"₹{total_gst:,.0f}"

            )









            # =====================
            # GST STACKED COLUMN
            # =====================


            fig_gst = px.bar(


                gst_data,


                x="YearMonth",


                y=[

                    "CGST",

                    "SGST"

                ],


                title="🧾 Monthly GST Collection Trend",


                barmode="stack",



                color_discrete_sequence=[


                    "#118DFF",


                    "#FFB000"


                ]


            )









            fig_gst.update_traces(



                hovertemplate=

                "GST Amount : ₹%{y:,.0f}"

                +

                "<extra></extra>"


            )










            fig_gst.update_layout(



                height=520,



                hovermode="x unified",



                xaxis_title="",



                yaxis_title="GST Amount",



                legend_title="Tax Type"



            )











            fig_gst = apply_chart_theme(


                fig_gst


            )











            st.plotly_chart(



                fig_gst,



                width="stretch",



                key="powerbi_gst_chart"



            )











            # =====================
            # GST INSIGHT
            # =====================


            peak_gst = (


                gst_data

                .assign(

                    Total_GST =

                    gst_data["CGST"]

                    +

                    gst_data["SGST"]

                )

                .sort_values(

                    "Total_GST",

                    ascending=False

                )

                .iloc[0]


            )










            st.success(

                f"""

🧾 Highest GST Collection


Month:

{peak_gst['YearMonth']}


Amount:

₹{peak_gst['Total_GST']:,.0f}

"""

            )









        else:



            st.info(

                "GST data unavailable"

            )
                # ===============================
        # POWER BI DISCOUNT IMPACT
        # ===============================


        if (

            "Discount_Amt" in df.columns

            and

            df["Discount_Amt"].sum() > 0

        ):


            st.subheader(

                "🏷 Discount Revenue Intelligence"

            )





            # ======================
            # SAMPLE DATA
            # ======================


            sample_df = (

                df[

                    [

                        "Discount_Amt",

                        revenue_col

                    ]

                ]

                .dropna()

                .sample(

                    min(

                        len(df),

                        5000

                    ),

                    random_state=42

                )

            )








            # ======================
            # KPI CARDS
            # ======================


            total_discount = (

                df["Discount_Amt"]

                .sum()

            )



            avg_discount = (

                df["Discount_Amt"]

                .mean()

            )



            discount_ratio = (

                total_discount

                /

                max(

                    df[revenue_col]

                    .sum(),

                    1

                )

                *

                100

            )







            c1,c2,c3 = st.columns(3)




            c1.metric(

                "Total Discount",

                f"₹{total_discount:,.0f}"

            )




            c2.metric(

                "Average Discount",

                f"₹{avg_discount:,.2f}"

            )




            c3.metric(

                "Discount Ratio",

                f"{discount_ratio:.2f}%"

            )










            # ======================
            # POWER BI BUBBLE CHART
            # ======================


            fig_discount = px.scatter(


                sample_df,


                x="Discount_Amt",


                y=revenue_col,


                size=revenue_col,


                color=revenue_col,


                title="Discount vs Revenue Impact Analysis",



                color_continuous_scale=[


                    "#00C2FF",


                    "#118DFF",


                    "#7C3AED",


                    "#FFB000",


                    "#FF1F3D"


                ],



                size_max=65


            )











            fig_discount.update_traces(



                marker=dict(

                    opacity=0.75

                ),




                hovertemplate=

                "<b>Discount:</b> ₹%{x:,.0f}<br>"

                +

                "Revenue : ₹%{y:,.0f}"

                +

                "<extra></extra>"


            )










            fig_discount.update_layout(



                height=550,


                showlegend=False,


                coloraxis_showscale=False,


                xaxis_title="Discount Given",


                yaxis_title="Revenue Generated"



            )











            fig_discount = apply_chart_theme(


                fig_discount


            )










            st.plotly_chart(


                fig_discount,


                width="stretch",


                key="powerbi_discount_analysis"


            )









            # ======================
            # BUSINESS INSIGHT
            # ======================


            highest_sale = (


                sample_df

                .sort_values(

                    revenue_col,

                    ascending=False

                )

                .iloc[0]


            )








            st.success(

                f"""

🏷 Discount Intelligence


Highest Revenue Transaction:


💰 Revenue:

₹{highest_sale[revenue_col]:,.0f}


🎯 Discount:

₹{highest_sale['Discount_Amt']:,.0f}

"""

            )






        else:



            st.info(

                "Discount data unavailable"

            )

        # ===============================
        # POWER BI DELIVERY INTELLIGENCE
        # ===============================


        if "Delivery_Charge" in df.columns:


            st.subheader(

                "🚚 Delivery Revenue Intelligence"

            )


            delivery = (

                df.groupby("YearMonth")

                ["Delivery_Charge"]

                .sum()

                .reset_index()

            )






            # =====================
            # KPI CARDS
            # =====================


            total_delivery = (

                delivery["Delivery_Charge"]

                .sum()

            )



            avg_delivery = (

                delivery["Delivery_Charge"]

                .mean()

            )





            c1,c2 = st.columns(2)




            c1.metric(

                "🚚 Total Delivery Revenue",

                f"₹{total_delivery:,.0f}"

            )




            c2.metric(

                "📦 Average Delivery",

                f"₹{avg_delivery:,.2f}"

            )









            # =====================
            # DELIVERY COLUMN CHART
            # =====================


            fig_delivery = px.bar(


                delivery,


                x="YearMonth",


                y="Delivery_Charge",


                color="Delivery_Charge",


                text_auto=True,


                title="🚚 Monthly Delivery Revenue",



                color_continuous_scale=[


                    "#06B6D4",


                    "#2563EB",


                    "#7C3AED",


                    "#EF4444"


                ]


            )









            fig_delivery.update_traces(


                texttemplate="₹%{y:,.0f}",


                textposition="outside",




                hovertemplate=

                "<b>Month:</b> %{x}<br>"

                +

                "Delivery Revenue : ₹%{y:,.0f}"

                +

                "<extra></extra>"


            )









            fig_delivery.update_layout(


                height=500,


                coloraxis_showscale=False,


                showlegend=False,


                xaxis_title="",


                yaxis_title="Delivery Revenue"


            )











            fig_delivery = apply_chart_theme(


                fig_delivery


            )










            st.plotly_chart(


                fig_delivery,


                width="stretch",


                key="delivery_revenue_chart"


            )










            # =====================
            # DELIVERY INSIGHT
            # =====================


            best_delivery = (

                delivery

                .sort_values(

                    "Delivery_Charge",

                    ascending=False

                )

                .iloc[0]

            )







            st.success(

                f"""

🚚 Best Delivery Month


{best_delivery['YearMonth']}


Revenue:


₹{best_delivery['Delivery_Charge']:,.0f}

"""

            )









        # ==================================================
        # POWER BI AI BUSINESS INSIGHTS
        # ==================================================


        st.subheader(

            "🤖 AI Business Intelligence Summary"

        )





        card1,card2,card3 = st.columns(3)






        if "best_category" in analytics:


            card1.metric(

                "🏆 Best Category",

                analytics["best_category"]

            )






        if "best_meal" in analytics:


            card2.metric(

                "🍽 Peak Meal",

                analytics["best_meal"]

            )







        if "best_payment" in analytics:


            card3.metric(

                "💳 Top Payment",

                analytics["best_payment"]

            )





    # ==================================================
    # POWER BI EXECUTIVE AI RECOMMENDATIONS
    # ==================================================


    st.divider()


    st.subheader(

        "💡 AI Executive Recommendations"

    )





    insight1, insight2, insight3 = st.columns(3)





    # ===============================
    # CATEGORY STRATEGY
    # ===============================


    if "best_category" in analytics:


        with insight1:


            st.metric(

                "📈 Revenue Focus",

                analytics["best_category"]

            )


            st.info(

                f"""

Your strongest revenue category is:

🏆 {analytics['best_category']}


Recommended Action:

Increase promotions, availability and focus campaigns.

"""

            )








    # ===============================
    # MEAL STRATEGY
    # ===============================


    if "best_meal" in analytics:


        with insight2:


            st.metric(

                "🍽 Peak Sales Window",

                analytics["best_meal"]

            )



            st.info(

                f"""

Peak performing meal period:


⏰ {analytics['best_meal']}


Recommended Action:


Optimize staffing and preparation.

"""

            )










    # ===============================
    # PAYMENT STRATEGY
    # ===============================


    if "best_payment" in analytics:


        with insight3:


            st.metric(

                "💳 Customer Preference",

                analytics["best_payment"]

            )



            st.info(

                f"""

Most preferred payment mode:


💳 {analytics['best_payment']}


Recommended Action:


Build loyalty offers around this segment.

"""

            )









    # ==================================================
    # WEEKDAY VS WEEKEND AI RECOMMENDATION
    # ==================================================


    if "week_analysis" in analytics:



        week_data = dict(


            zip(


                analytics["week_analysis"]["Is_Weekend"],


                analytics["week_analysis"][revenue_col]


            )


        )







        weekend = week_data.get(

            "Weekend",

            0

        )




        weekday = week_data.get(

            "Weekday",

            0

        )









        st.subheader(

            "📅 Sales Timing Recommendation"

        )








        if weekend > weekday:



            difference = (

                (

                    weekend

                    -

                    weekday

                )

                /

                max(

                    weekday,

                    1

                )

                *

                100

            )







            st.success(

                f"""

🚀 Weekend Opportunity Detected


Weekend sales are higher by:


{difference:.2f}%


Recommended Actions:


✔ Increase weekend offers


✔ Maintain higher stock


✔ Add additional staff


"""

            )








        else:




            difference = (

                (

                    weekday

                    -

                    weekend

                )

                /

                max(

                    weekend,

                    1

                )

                *

                100

            )








            st.success(

                f"""

📊 Weekday Dominance Detected


Weekday sales are higher by:


{difference:.2f}%


Recommended Actions:


✔ Improve weekday loyalty programs


✔ Create repeat customer campaigns


✔ Maintain weekday efficiency


"""

            )