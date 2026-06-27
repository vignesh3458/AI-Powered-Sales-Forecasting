import streamlit.components.v1 as components

import pandas as pd



def kpi_card(

        title,

        value,

        change=None,

        icon="📊"

):


    growth_html = ""



    if change is not None and not pd.isna(change):


        if change >= 0:


            color="#22C55E"

            arrow="▲"


        else:


            color="#EF4444"

            arrow="▼"



        growth_html=f"""

        <div class="growth"
        style="color:{color};">

        {arrow} {change:.2f}%

        </div>

        """




    html=f"""


    <style>


    .card{{


        background:

        linear-gradient(

        135deg,

        #1e293b,

        #020617

        );


        border-radius:22px;


        padding:25px;


        height:150px;


        border:

        1px solid rgba(255,255,255,0.15);


        box-shadow:

        0px 15px 35px rgba(0,0,0,0.35);


        font-family:Segoe UI;


    }}



    .top{{


        display:flex;


        gap:12px;


        align-items:center;


    }}



    .icon{{


        font-size:30px;


    }}



    .title{{


        color:#94A3B8;


        font-size:16px;


        font-weight:700;


    }}



    .value{{


        margin-top:20px;


        color:white;


        font-size:30px;


        font-weight:900;


    }}



    .growth{{


        margin-top:12px;


        font-size:16px;


        font-weight:800;


    }}



    </style>





    <div class="card">


        <div class="top">


            <div class="icon">

            {icon}

            </div>



            <div class="title">

            {title}

            </div>


        </div>




        <div class="value">

        {value}

        </div>




        {growth_html}



    </div>


    """



    components.html(

        html,

        height=190

    )