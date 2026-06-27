from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet



def create_pdf(
        filename,
        total_revenue,
        total_transactions,
        avg_bill,
        total_items,
        forecast_avg,
        best_category,
        best_meal,
        model_accuracy=None,
        mape=None
):


    doc = SimpleDocTemplate(
        filename
    )


    styles = getSampleStyleSheet()


    content=[]



    # ==========================
    # TITLE
    # ==========================


    content.append(

        Paragraph(
            "AI Sales Intelligence Report",
            styles["Title"]
        )

    )


    content.append(

        Paragraph(
            "Restaurant Forecast & Analytics System",
            styles["Heading2"]
        )

    )


    content.append(
        Spacer(1,20)
    )





    # ==========================
    # KPI TABLE
    # ==========================


    kpi_data=[


        [
            "Metric",
            "Value"
        ],


        [
            "Net Revenue",
            f"₹{total_revenue:,.2f}"
        ],


        [
            "Transactions",
            f"{total_transactions:,}"
        ],


        [
            "Average Bill",
            f"₹{avg_bill:,.2f}"
        ],


        [
            "Items Sold",
            f"{total_items:,}"
        ]

    ]



    table=Table(
        kpi_data,
        colWidths=[220,220]
    )



    table.setStyle(

        TableStyle(

            [

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

            ]

        )

    )



    content.append(
        table
    )



    content.append(
        Spacer(1,25)
    )





    # ==========================
    # FORECAST
    # ==========================


    content.append(

        Paragraph(
            "Forecast Summary",
            styles["Heading2"]
        )

    )


    content.append(

        Paragraph(

            f"""

            Average Predicted Revenue:
            ₹{forecast_avg:,.2f}

            """,

            styles["BodyText"]

        )

    )



    content.append(
        Spacer(1,20)
    )






    # ==========================
    # MODEL PERFORMANCE
    # ==========================


    if model_accuracy is not None:


        content.append(

            Paragraph(
                "AI Model Performance",
                styles["Heading2"]
            )

        )



        model_table=[


            [
                "Metric",
                "Value"
            ],


            [
                "Accuracy",
                f"{model_accuracy}%"
            ],


            [
                "MAPE",
                f"{mape}%"
            ]

        ]



        mt=Table(
            model_table,
            colWidths=[220,220]
        )


        mt.setStyle(

            TableStyle(

                [

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("ALIGN",(0,0),(-1,-1),"CENTER")

                ]

            )

        )



        content.append(mt)







    content.append(
        Spacer(1,25)
    )





    # ==========================
    # BUSINESS INSIGHTS
    # ==========================


    content.append(

        Paragraph(
            "AI Business Insights",
            styles["Heading2"]
        )

    )


    content.append(

        Paragraph(

            f"""

            Best Category:
            {best_category}

            <br/>

            Best Meal Period:
            {best_meal}


            """,

            styles["BodyText"]

        )

    )






    # ==========================
    # BUILD
    # ==========================


    doc.build(

        content

    )