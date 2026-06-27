from fastapi import FastAPI, Body, HTTPException

from backend.database import (
    get_sales_data,
    insert_sales_data,
    insert_staging_data,
    approve_staging_data,
    get_model_update_time
)

import pandas as pd

from processing.schema_mapper import map_schema
from forecasting.forecast_model import generate_forecast
from processing.data_processor import process_sales_data
import numpy as np



app = FastAPI(


    title="Restaurant Analytics API"


)



@app.get("/sales")


def sales(
    limit:int=100
):


    df = get_sales_data()


    df = df.replace(
        {
            np.nan:None,
            np.inf:None,
            -np.inf:None
        }
    )


    df = df.head(
        limit
    )


    df["Date"] = df["Date"].astype(str)


    return {


            "total_records":len(df),


            "data":

            df.to_dict(
                orient="records"
            )

        }

@app.get("/summary")


def summary():


    df=get_sales_data()


    return {


        "total_revenue":

        float(
            df["Net_Revenue"].sum()
        ),


        "transactions":

        len(df),


        "total_items":

        int(
            df["Quantity"].sum()
        )


    }
@app.get("/forecast")


def forecast_api():


    try:


        df = get_sales_data()


        model_version = get_model_update_time()



        forecast = generate_forecast(

            df,

            model_version=model_version,

            periods=30

        )




        return {


            "status":"success",


            "forecast":

            forecast[
                [
                    "ds",
                    "yhat",
                    "yhat_lower",
                    "yhat_upper"
                ]
            ]
            .replace(
                {
                    np.nan:None
                }
            )
            .to_dict(
                orient="records"
            )

        }




    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
    
@app.post("/upload-sales")


def upload_sales(

    data: list = Body(...)

):


    try:


        # ==============================
        # CHECK EMPTY JSON
        # ==============================


        if len(data) == 0:


            raise HTTPException(

                status_code=400,

                detail="Empty JSON file received"

            )





        # ==============================
        # JSON TO DATAFRAME
        # ==============================


        df = pd.DataFrame(

            data

        )





        if df.empty:


            raise HTTPException(

                status_code=400,

                detail="Unable to convert JSON"

            )


        # ==============================
        # DYNAMIC COLUMN MAPPING FIRST
        # ==============================


        df = map_schema(

            df

        )




        # ==============================
        # CLEAN + PROCESS DATA
        # ==============================


        df = process_sales_data(

            df

        )




    
        # ==============================
        # REQUIRED COLUMN CHECK
        # ==============================


        required_columns = [

            "Date",

            "Total_Billed"

        ]





        missing_columns = [


            col


            for col in required_columns


            if col not in df.columns


        ]






        if missing_columns:


            raise HTTPException(

                status_code=400,


                detail=f"Missing required columns: {missing_columns}"

            )








        # ==============================
        # REMOVE BAD ROWS
        # ==============================



        df = df.dropna(

            subset=[

                "Date",

                "Total_Billed"

            ]

        )







        if df.empty:


            raise HTTPException(

                status_code=400,

                detail="No valid rows after cleaning"

            )








        # ==============================
        # INSERT INTO POSTGRESQL
        # ==============================

        insert_staging_data(

            df

        )








        return {


            "status":"success",


            "message":

            "JSON validated and saved successfully",



            "columns_detected":

            list(df.columns),



            "records_added":

            len(df)


        }







    except HTTPException:


        raise







    except Exception as e:


        raise HTTPException(

            status_code=500,


            detail=str(e)

        )
    
@app.post("/approve-sales")


def approve_sales():


        try:


            approve_staging_data()


            return {


                "status":"success",


                "message":

                "Staging data approved and moved to production"


            }


        except Exception as e:


            raise HTTPException(

                status_code=500,

                detail=str(e)

            )
