# ============================
# POWER BI ENTERPRISE CHART THEME
# ============================


POWERBI_COLORS = [

    "#118DFF",
    "#12239E",
    "#E66C37",
    "#6B007B",
    "#E044A7",
    "#744EC2",
    "#D9B300",
    "#D64550",
    "#197278",
    "#1AAB40"

]





def apply_chart_theme(fig):


    fig.update_layout(


        template="plotly_dark",



        paper_bgcolor="rgba(0,0,0,0)",


        plot_bgcolor="rgba(0,0,0,0)",




        font=dict(

            family="Segoe UI",

            size=14,

            color="#E5E7EB"

        ),




        title=dict(

            font=dict(

                size=20,

                color="#F8FAFC"

            ),

            x=0.02

        ),




        legend=dict(

            orientation="h",

            y=-0.25,

            x=0.5,

            xanchor="center",

            bgcolor="rgba(0,0,0,0)"

        ),




        hoverlabel=dict(

            bgcolor="#020617",

            bordercolor="#334155",

            font=dict(

                color="white",

                size=14

            )

        ),



        hovermode="x unified",



        margin=dict(

            l=30,

            r=30,

            t=60,

            b=40

        )

    )





    fig.update_xaxes(


        showgrid=False,


        zeroline=False,


        tickfont=dict(

            color="#CBD5E1"

        )

    )




    fig.update_yaxes(


        gridcolor="rgba(255,255,255,0.08)",


        zeroline=False,


        tickfont=dict(

            color="#CBD5E1"

        )

    )




    return fig