import streamlit as st

import plotly.express as px


from analytics.anomaly_detector import (
    detect_anomalies
)


from components.chart_theme import (
    apply_chart_theme
)




def show_anomalies(df):


    st.subheader(

        "AI Anomaly Detection"

    )



    anomalies=detect_anomalies(

        df

    )



    if anomalies.empty:


        st.success(

            "No abnormal sales patterns detected"

        )


        return



    st.warning(

        f"{len(anomalies)} unusual business days found"

    )




    fig=px.scatter(

        anomalies,

        x="Date",

        y="Revenue",

        size="Revenue",

        hover_data=[

            "Status"

        ],

        title="Detected Revenue Anomalies"

    )



    fig=apply_chart_theme(

        fig

    )



    st.plotly_chart(

        fig,

        width="stretch"

    )




    st.dataframe(

        anomalies,

        use_container_width=True

    )