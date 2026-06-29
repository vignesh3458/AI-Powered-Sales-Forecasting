import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    Image,
    TableStyle
)


from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER



# =====================================================
# CREATE CHART IMAGE
# =====================================================

def chart_image(fig):


    img = BytesIO()


    fig.write_image(
        img,
        format="png"
    )


    img.seek(0)


    return img



# =====================================================
# PAGE BORDER
# =====================================================

def add_page_border(canvas, doc):


    canvas.saveState()


    canvas.setLineWidth(2)


    canvas.rect(

        25,

        25,

        doc.pagesize[0] - 50,

        doc.pagesize[1] - 50

    )


    canvas.restoreState()

# =====================================================
# PDF REPORT
# =====================================================

def create_pdf_report(df):

    revenue_col = (

    "Net_Revenue"

    if "Net_Revenue" in df.columns

    else "Total_Billed"

)


    buffer = BytesIO()


    pdf = SimpleDocTemplate(buffer)


    styles = getSampleStyleSheet()
        # Times New Roman Equivalent
    # ReportLab built-in serif font

    styles["Title"].fontName = "Times-Bold"
    styles["Title"].alignment = TA_CENTER


    styles["Heading2"].fontName = "Times-Bold"


    styles["Normal"].fontName = "Times-Roman"

    content=[]



    content.append(
        Paragraph(
            "AI SALES INTELLIGENCE REPORT",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )



    # --------------------------
    # KPI SECTION
    # --------------------------


    kpis=[

        ["Metric","Value"],

        [
            "Net Revenue",
            f"₹{df[revenue_col].sum():,.2f}"
        ],

        [
            "Transactions",
            len(df)
        ],

        [
            "Average Bill",
            f"₹{df[revenue_col].mean():.2f}"
        ],

        [
            "Items Sold",
            int(df["Quantity"].sum())
        ]

    ]


    content.append(
        Paragraph(
            "Executive KPI Summary",
            styles["Heading2"]
        )
    )


    kpi_table = Table(
        kpis
    )


    kpi_table.setStyle(

        TableStyle(

            [

                ("GRID",(0,0),(-1,-1),1,colors.black),


                ("FONT",(0,0),(-1,-1),"Times-Roman"),


                ("FONT",(0,0),(-1,0),"Times-Bold"),


                ("ALIGN",(0,0),(-1,-1),"CENTER"),


                ("BOTTOMPADDING",(0,0),(-1,-1),10)

            ]

        )

    )


    content.append(
        kpi_table
    )


    content.append(
        Spacer(1,20)
    )




    # ==================================================
    # MONTHLY REVENUE CHART
    # ==================================================


    monthly=(

        df.groupby("YearMonth")
        [revenue_col]
        .sum()
        .reset_index()

    )


    fig1=px.line(

        monthly,

        x="YearMonth",

        y=revenue_col,

        title="Monthly Revenue Trend"

    )


    content.append(

        Image(
            chart_image(fig1),
            width=400,
            height=250
        )

    )


    content.append(
        Spacer(1,20)
    )




    # ==================================================
    # CATEGORY CHART
    # ==================================================


    category=(

        df.groupby("Category")
        [revenue_col]
        .sum()
        .reset_index()

    )



    fig2=px.bar(

        category,

        x="Category",

        y=revenue_col,

        title="Revenue by Category"

    )



    content.append(

        Image(

            chart_image(fig2),

            width=400,

            height=250

        )

    )



    content.append(
        Spacer(1,20)
    )



    # ==================================================
    # TOP ITEMS
    # ==================================================


    products=(

        df.groupby("Item_Name")
        ["Quantity"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()

    )



    fig3=px.bar(

        products,

        x="Item_Name",

        y="Quantity",

        title="Top Selling Items"

    )



    content.append(

        Image(

            chart_image(fig3),

            width=400,

            height=250

        )

    )



    content.append(
        Spacer(1,20)
    )



    # --------------------------
    # INSIGHTS
    # --------------------------


    best_category=(

        df.groupby("Category")
        [revenue_col]
        .sum()
        .idxmax()

    )



    best_meal=(

        df.groupby("Meal_Period")
        [revenue_col]
        .sum()
        .idxmax()

    )



    content.append(

        Paragraph(

            "AI Business Insights",

            styles["Heading2"]

        )

    )



    content.append(

        Paragraph(

            f"""
            Best Category : {best_category}
            <br/>

            Best Meal Period : {best_meal}
            """,

            styles["Normal"]

        )

    )



    pdf.build(

        content,

        onFirstPage=add_page_border,

        onLaterPages=add_page_border

    )


    buffer.seek(0)


    return buffer





# =====================================================
# EXCEL REPORT
# =====================================================

def create_excel_report(df):

    revenue_col = (
        "Net_Revenue"
        if "Net_Revenue" in df.columns
        else "Total_Billed"
    )

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        # ======================
        # KPI SUMMARY
        # ======================
        summary = pd.DataFrame({
            "Metric": [
                "Revenue",
                "Transactions",
                "Average Bill",
                "Items Sold"
            ],
            "Value": [
                df[revenue_col].sum(),
                len(df),
                df[revenue_col].mean(),
                df["Quantity"].sum()
            ]
        })

        summary.to_excel(
            writer,
            sheet_name="KPI Summary",
            index=False
        )

        # ======================
        # CATEGORY REPORT
        # ======================
        category = (
            df.groupby("Category")[revenue_col]
            .sum()
            .reset_index()
        )

        category.to_excel(
            writer,
            sheet_name="Category Analysis",
            index=False
        )

        # ======================
        # PRODUCT REPORT
        # ======================
        product = (
            df.groupby("Item_Name")["Quantity"]
            .sum()
            .reset_index()
        )

        product.to_excel(
            writer,
            sheet_name="Product Analysis",
            index=False
        )

        # ======================
        # MEAL REPORT
        # ======================
        meal = (
            df.groupby("Meal_Period")[revenue_col]
            .sum()
            .reset_index()
        )

        meal.to_excel(
            writer,
            sheet_name="Meal Analysis",
            index=False
        )

        # ======================
        # PAYMENT REPORT
        # ======================
        payment = (
            df.groupby("Payment_Method")[revenue_col]
            .sum()
            .reset_index()
        )

        payment.to_excel(
            writer,
            sheet_name="Payment Analysis",
            index=False
        )

        # ======================
        # RAW DATA
        # ======================
        df.head(50000).to_excel(
            writer,
            sheet_name="Raw Sample",
            index=False
        )

    output.seek(0)

    return output.getvalue()

# =====================================================
# UI
# =====================================================


def show_reports(df):


    st.subheader(
        "📑 AI Business Report Center"
    )


    pdf_bytes = create_pdf_report(df)

    if pdf_bytes:

        st.download_button(
            label="📄 Download Complete PDF Report",
            data=pdf_bytes,
            file_name="AI_Sales_Report.pdf",
            mime="application/pdf"
        )

    else:

        st.error("Failed to generate PDF report.")



    excel_bytes = create_excel_report(df)

    if excel_bytes:

        st.download_button(
            label="📊 Download Complete Excel Report",
            data=excel_bytes,
            file_name="AI_Sales_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:

        st.error("Failed to generate Excel report.")