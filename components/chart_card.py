import streamlit as st



def chart_card(
        title,
        fig,
        key=None
):


    st.markdown(

        f"""

<div class="chart-heading">

{title}

</div>


        """,

        unsafe_allow_html=True

    )



    st.plotly_chart(

        fig,

        use_container_width=True,

        key=key

    )