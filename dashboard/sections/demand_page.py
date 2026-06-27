import streamlit as st


from analytics.demand_engine import (

    analyze_demand

)




def show_demand(df):


    st.subheader(

        "Customer Demand Intelligence"

    )



    result = analyze_demand(

        df

    )



    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "🔥 Peak Hour",

        result["Peak Hour"]

    )



    c2.metric(

        "🍽 Best Meal",

        result["Best Meal"]

    )



    c3.metric(

        "🏆 Top Product",

        result["Best Item"]

    )



    c4.metric(

        "📈 Demand Score",

        f"{result['Demand Score']}/100"

    )




    # ======================
    # AI MESSAGE
    # ======================


    st.subheader(

        "💡 AI Demand Insight"

    )



    if result["Demand Score"] >=80:


        st.success(

            """
            Customer demand is strong.

            Recommended:

            ✔ Maintain stock levels

            ✔ Increase staff during peak hours

            ✔ Promote best selling items
            """

        )


    else:


        st.warning(

            """
            Demand can be improved.

            Recommended:

            ✔ Create offers

            ✔ Improve low performing periods

            ✔ Analyze customer patterns
            """

        )