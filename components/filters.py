import streamlit as st



def apply_filters(

        df,

        key_prefix,

        show_forecast=False

):


    st.sidebar.title(

        "⚙ Dashboard Filters"

    )


    # ============================
    # CREATE SINGLE BOOLEAN MASK
    # ============================


    mask = (

        df.index == df.index

    )

    # ============================
    # YEAR FILTER
    # ============================


    if "Year" in df.columns:


        years = sorted(

            df["Year"]

            .dropna()

            .unique()

        )


        year_filter = st.sidebar.multiselect(

            "Year",

            options=years,

            default=years,

            key=f"{key_prefix}_year"

        )


        mask = (

            mask

            &

            df["Year"].isin(

                year_filter

            )

        )




    # ============================
    # MONTH FILTER
    # ============================


    if "Month_Name" in df.columns:


        month_order = [

            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"

        ]


        months = [

            m for m in month_order

            if m in df["Month_Name"].values

        ]



    # ============================
    # MEAL FILTER
    # ============================


    if "Meal_Period" in df.columns:


        meals = (

            df["Meal_Period"]

            .dropna()

            .unique()

        )


        meal_filter = st.sidebar.multiselect(

            "Meal Period",

            options=meals,

            default=meals,

            key=f"{key_prefix}_meal"

        )



        mask = (

            mask

            &

            df["Meal_Period"].isin(

                meal_filter

            )

        )




    # ============================
    # CATEGORY FILTER
    # ============================


    if "Category" in df.columns:


        categories = (

            df["Category"]

            .dropna()

            .unique()

        )



        category_filter = st.sidebar.multiselect(

            "Category",

            options=categories,

            default=categories,

            key=f"{key_prefix}_category"

        )



        mask = (

            mask

            &

            df["Category"].isin(

                category_filter

            )

        )




    # ============================
    # PAYMENT FILTER
    # ============================


    if "Payment_Method" in df.columns:


        payments = (

            df["Payment_Method"]

            .dropna()

            .unique()

        )



        payment_filter = st.sidebar.multiselect(

            "Payment Method",

            options=payments,

            default=payments,

            key=f"{key_prefix}_payment"

        )



        mask = (

            mask

            &

            df["Payment_Method"].isin(

                payment_filter

            )

        )




    # ============================
    # APPLY FILTER ONCE ONLY
    # ============================


    filtered_df = (

        df.loc[mask]

    )





    # ============================
    # FORECAST SETTINGS
    # ============================


    forecast_days = None


    forecast_category = None



    if show_forecast:


        st.sidebar.divider()


        st.sidebar.subheader(

            "🔮 Forecast Settings"

        )



        forecast_days = st.sidebar.slider(

            "Forecast Days",

            min_value=7,

            max_value=90,

            value=30,

            key=f"{key_prefix}_forecast_days"

        )




        if "Category" in df.columns:


            forecast_category = st.sidebar.selectbox(

                "Forecast Category",

                [

                    "All"

                ]

                +

                sorted(

                        filtered_df["Category"]

                        .dropna()

                        .unique()

                        .tolist()

                    ),

                key=f"{key_prefix}_forecast_category"

            )


        else:


            forecast_category = "All"





    return (

        filtered_df,

        forecast_days,

        forecast_category

    )