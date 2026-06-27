import sys
import os
from pathlib import Path


# ==================================
# PROJECT PATH
# ==================================

ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT))



# ==================================
# IMPORTS
# ==================================

import streamlit as st

import pandas as pd

import streamlit.components.v1 as components


from streamlit_option_menu import option_menu



from components.styling import load_css

from components.filters import apply_filters



from database.company_loader import load_company_data



from dashboard.sections.overview import (

    show_overview

)


from dashboard.sections.analytics import (

    show_analytics

)


from dashboard.sections.forecast_page import (

    show_forecast

)


from dashboard.sections.model_monitoring import (

    show_model_monitoring

)


from dashboard.sections.ai_assistant import (

    show_ai_assistant

)


from dashboard.sections.reports_page import (

    show_reports

)


from dashboard.sections.anomaly_page import (

    show_anomalies

)


from dashboard.sections.demand_page import (

    show_demand

)





# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(

    page_title=
    "AI Sales Forecasting",

    layout="wide",

    initial_sidebar_state="expanded"

)



# LOAD CSS

load_css()


# ==================================
# DATA LOADING
# ==================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)


def get_data():


    return load_company_data()





col1, col2 = st.columns([8, 1])

with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

df = get_data()



if df is None or df.empty:


    st.error(

        "Dataset not loaded"

    )


    st.stop()





# ==================================
# DATE FIX
# ==================================

df["Date"] = pd.to_datetime(

    df["Date"],

    errors="coerce"

)



df=df.dropna(

    subset=["Date"]

)





df["Day_Name"] = (

    df["Date"]

    .dt.day_name()

)





# ----------------------------
# TITLE
# ----------------------------

# ----------------------------
# DASHBOARD TITLE
# ----------------------------
st.markdown(
    """

<div class="dashboard-title">

<h1>
📊 Sales Analytics Dashboard
</h1>


<p>
AI Powered Forecasting • Analytics • Business Intelligence
</p>


</div>

""",

unsafe_allow_html=True

)

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:



    st.markdown(

        """

        <div class="sidebar-logo">

            Navigation Bar

        </div>

        """,

        unsafe_allow_html=True

    )




    page = option_menu(


        menu_title="WORKSPACE",



        options=[


            "Overview",


            "Analytics",


            "Forecast",


            "Model Performance",


            "AI Anomaly Detection",


            "Demand Intelligence",


            "AI Assistant",


            "Reports"

        ],




        icons=[


            "house-fill",


            "bar-chart-fill",


            "graph-up-arrow",


            "cpu-fill",


            "exclamation-triangle-fill",


            "activity",


            "robot",


            "file-earmark-text-fill"

        ],




        default_index=0,



        styles={



            "container":{

                "background-color":"#0B1120"

            },



            "icon":{

                "color":"#EF233C",

                "font-size":"22px"

            },



            "nav-link":{


                "font-size":"17px",

                "font-weight":"700",

                "color":"#E5E7EB",

                "padding":"14px",

                "border-radius":"15px"

            },



            "nav-link-selected":{


                "background-color":"#EF233C",

                "color":"white"

            }

        }

    )






# ==================================
# AUTO SCROLL
# ==================================

components.html(

    """

    <script>

    window.parent.scrollTo(

    {

    top:0,

    behavior:"smooth"

    }

    );

    </script>

    """,

    height=0

)







# ==================================
# ROUTING
# ==================================

if page=="Overview":


    filtered_df,_,_=apply_filters(

        df,

        "overview"

    )


    show_overview(

        filtered_df

    )





elif page=="Analytics":



    filtered_df,_,_=apply_filters(

        df,

        "analytics"

    )


    show_analytics(

        filtered_df

    )






elif page=="Forecast":



    filtered_df,_,_=apply_filters(

        df,

        "forecast",

        show_forecast=True

    )


    show_forecast(

        filtered_df

    )






elif page=="Model Performance":


    show_model_monitoring(

        df

    )






elif page=="AI Anomaly Detection":


    show_anomalies(

        df

    )







elif page=="Demand Intelligence":


    show_demand(

        df

    )







elif page=="AI Assistant":


    show_ai_assistant(

        df

    )







elif page=="Reports":


    show_reports(

        df

    )