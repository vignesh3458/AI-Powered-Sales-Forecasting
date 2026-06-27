def map_schema(df):


    rename_map = {}



    for column in df.columns:


        clean = (

            str(column)

            .lower()

            .strip()

            .replace(" ","_")

        )



       # =====================
        # DATE
        # =====================

        if clean in [

            "date",
            "order_date",
            "bill_date",
            "billdatetime",
            "bill_date_time",
            "created_at",
            "billororderdatetime",
            "billordatetime",
            "bill_time"

        ]:

            rename_map[column] = "Date"




        # =====================
        # BILL ID
        # =====================


        elif clean in [

            "billno",
            "bill_no",
            "invoice_no",
            "invoice_id",
            "order_id"

        ]:


            rename_map[column] = "BillNo"







        # =====================
        # REVENUE
        # =====================


        elif clean in [

            "sales",
            "amount",
            "revenue",
            "billamount",
            "bill_amount",
            "total_amount",
            "total_bill"

        ]:


            rename_map[column] = "Total_Billed"








        # =====================
        # ITEM
        # =====================


        elif clean in [

            "item",
            "itemname",
            "item_name",
            "product",
            "product_name",
            "food_name"

        ]:


            rename_map[column] = "Item_Name"









        # =====================
        # CATEGORY
        # =====================


        elif clean in [

            "category",
            "classification",
            "classificationname",
            "item_category"

        ]:


            rename_map[column] = "Category"








        # =====================
        # QUANTITY
        # =====================


        elif clean in [

            "qty",
            "quantity",
            "item_qty"

        ]:


            rename_map[column] = "Quantity"








        # =====================
        # DISCOUNT
        # =====================


        elif clean in [

            "discount",
            "discount_amount",
            "totaldiscountamount"

        ]:


            rename_map[column] = "Discount_Amt"








        # =====================
        # TAX
        # =====================


        elif clean in [

            "tax",
            "gst",
            "total_tax",
            "totaltaxamount"

        ]:


            rename_map[column] = "Tax_Amt"








        # =====================
        # CHARGES
        # =====================


        elif clean in [

            "service_charge",
            "totalchargeamount"

        ]:


            rename_map[column] = "Service_Charge"



        elif clean in [

            "delivery_charge"

        ]:


            rename_map[column] = "Delivery_Charge"








       # =====================
        # PAYMENT
        # =====================

        elif clean in [

            "payment",
            "payment_mode",
            "paymentmethod",
            "paymentmode"

        ]:

            rename_map[column] = "Payment_Method"









        # =====================
        # WEATHER
        # =====================


        elif clean == "weather":


            rename_map[column] = "Weather"






    df = df.rename(

    columns=rename_map

)

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    return df
