import streamlit as st


def load_css():


    st.markdown(
        """

<style>


/* ======================
APP BACKGROUND
====================== */


.stApp{


background:

linear-gradient(

135deg,

#020617,

#0F172A

);


color:white;


}




.block-container{


padding-top:2rem;

padding-bottom:2rem;


}





/* ======================
SIDEBAR
====================== */


section[data-testid="stSidebar"]{


background:

#020617;


border-right:

1px solid rgba(255,255,255,0.1);


}







/* ======================
TEXT
====================== */


h1,h2,h3,p{


color:white;


}




/* ======================
CHART CARD
====================== */



.chart-box{


background:

rgba(255,255,255,0.05);


border-radius:25px;


padding:20px;


border:

1px solid rgba(255,255,255,0.1);


box-shadow:

0px 15px 40px rgba(0,0,0,0.35);


}



.chart-heading{


font-size:20px;

font-weight:900;

margin-bottom:15px;


}








/* ======================
BUTTONS
====================== */



.stButton button,


.stDownloadButton button{


background:

linear-gradient(

90deg,

#EF233C,

#D90429

);


border:none;


border-radius:14px;


color:white;


font-weight:800;


}


/* ======================
DASHBOARD TITLE
====================== */


.dashboard-title{


text-align:center;


margin-bottom:35px;


padding:25px;


background:

linear-gradient(

135deg,

rgba(30,41,59,0.9),

rgba(15,23,42,0.95)

);


border-radius:25px;


border:

1px solid rgba(255,255,255,0.1);


box-shadow:

0px 15px 40px rgba(0,0,0,0.35);


}




.dashboard-title h1{


font-size:42px;


font-weight:900;


color:#F8FAFC;


}




.dashboard-title p{


font-size:18px;


font-weight:600;


color:#94A3B8;


}




</style>


        """,

        unsafe_allow_html=True

    )