import streamlit as st

import pandas as pd

import plotly.express as px



from components.kpi_card import kpi_card


from components.chart_card import chart_card


from components.chart_theme import (

    apply_chart_theme,

    POWERBI_COLORS

)






def show_overview(df):


    # ==========================
    # TITLE
    # ==========================


    st.subheader(
        "AI Sales Intelligence Dashboard"
    )


    st.caption(
        "Restaurant Revenue • Customer • Forecast Intelligence"
    )





    # ==========================
    # REVENUE COLUMN
    # ==========================


    revenue_col = (

        "Net_Revenue"

        if "Net_Revenue" in df.columns

        else "Total_Billed"

    )





    # ==========================
    # KPI CALCULATION
    # ==========================


    total_revenue = (

        df[revenue_col]

        .sum()

    )



    total_items = (

        df["Quantity"]

        .sum()

    )



    transactions = (

        df["BillNo"].nunique()

        if "BillNo" in df.columns

        else len(df)

    )



    avg_bill = (

        total_revenue

        /

        max(transactions,1)

    )







    # ==========================
    # GROWTH
    # ==========================


    agg_dict = {
    revenue_col: "sum",
    "Quantity": "sum"
    }

    if "BillNo" in df.columns:
        agg_dict["BillNo"] = "nunique"

    monthly = (
        df.groupby("YearMonth")
        .agg(agg_dict)
        .sort_index()
    )

    if "BillNo" not in monthly.columns:
        monthly["BillNo"] = (
            df.groupby("YearMonth").size()
        )





    if len(monthly)>=2:


        revenue_growth = (

            (

                monthly[revenue_col].iloc[-1]

                -

                monthly[revenue_col].iloc[-2]

            )

            /

            max(monthly[revenue_col].iloc[-2],1)

            *

            100

        )




        item_growth = (

            (

                monthly["Quantity"].iloc[-1]

                -

                monthly["Quantity"].iloc[-2]

            )

            /

            max(monthly["Quantity"].iloc[-2],1)

            *

            100

        )




        transaction_growth = (

            (

                monthly["BillNo"].iloc[-1]

                -

                monthly["BillNo"].iloc[-2]

            )

            /

            max(monthly["BillNo"].iloc[-2],1)

            *

            100

        )




        current_avg = (

            monthly[revenue_col].iloc[-1]

            /

            max(monthly["BillNo"].iloc[-1],1)

        )



        previous_avg = (

            monthly[revenue_col].iloc[-2]

            /

            max(monthly["BillNo"].iloc[-2],1)

        )



        avg_growth = (

            (

                current_avg

                -

                previous_avg

            )

            /

            max(previous_avg,1)

            *

            100

        )



    else:


        revenue_growth=0

        item_growth=0

        transaction_growth=0

        avg_growth=0







    # ==========================
    # KPI CARDS
    # ==========================


    c1,c2,c3,c4 = st.columns(4)



    with c1:


        kpi_card(

            "Revenue",

            f"₹{total_revenue/10000000:.2f} Cr",

            revenue_growth,

            "💰"

        )




    with c2:


        kpi_card(

            "Items Sold",

            f"{total_items/1000000:.2f}M",

            item_growth,

            "🍽️"

        )





    with c3:


        kpi_card(

            "Average Bill",

            f"₹{avg_bill:.2f}",

            avg_growth,

            "🧾"

        )





    with c4:


        kpi_card(

            "Orders",

            f"{transactions/1000000:.2f}M",

            transaction_growth,

            "🛒"

        )








    st.divider()







    # ==========================
    # INSIGHTS
    # ==========================


    best_category = (

        df.groupby("Category")

        [revenue_col]

        .sum()

        .idxmax()

    )



    best_product = (

        df.groupby("Item_Name")

        ["Quantity"]

        .sum()

        .idxmax()

    )



    best_day = (

        df.groupby("Day_Name")

        [revenue_col]

        .sum()

        .idxmax()

    )





    a,b,c = st.columns(3)



    with a:


        kpi_card(

            "Top Category",

            best_category,

            None,

            "🏆"

        )




    with b:


        kpi_card(

            "Best Product",

            best_product,

            None,

            "🔥"

        )




    with c:


        kpi_card(

            "Best Day",

            best_day,

            None,

            "📅"

        )








    st.divider()









    # ==========================
    # REVENUE CHART
    # ==========================


    revenue_data = (

        df.groupby("YearMonth")

        [revenue_col]

        .sum()

        .reset_index()

    )




    fig1 = px.area(

        revenue_data,

        x="YearMonth",

        y=revenue_col,

        markers=True

    )



    fig1.update_traces(

        line=dict(

            width=4,

            shape="spline"

        )

    )



    fig1 = apply_chart_theme(fig1)








    # ==========================
    # CATEGORY CHART
    # ==========================


    category = (

        df.groupby("Category")

        [revenue_col]

        .sum()

        .nlargest(8)

        .reset_index()

    )




    fig2 = px.pie(

        category,

        names="Category",

        values=revenue_col,

        hole=0.6,

        color_discrete_sequence=POWERBI_COLORS

    )



    fig2 = apply_chart_theme(fig2)








    left,right = st.columns(

        [2,1]

    )



    with left:


        chart_card(

            "📈 Revenue Trend",

            fig1,

            "revenue_chart"

        )



    with right:


        chart_card(

            "🍽 Revenue Mix",

            fig2,

            "category_chart"

        )








    st.divider()








    # ==========================
    # DATA
    # ==========================


    st.subheader(

        "📋 Dataset Preview"

    )



    st.dataframe(

        df.head(20),

        use_container_width=True

    )