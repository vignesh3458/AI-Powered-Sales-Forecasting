import pandas as pd

from processing.schema_mapper import map_schema
from processing.data_processor import process_sales_data

from backend.database import insert_staging_data


# ==========================================================
# PROCESS DATAFRAME
# ==========================================================

def process_uploaded_dataframe(df, truncate=False):

    if df is None or df.empty:
        return 0

    df = map_schema(df)

    df = process_sales_data(df)

    if df.empty:
        return 0

    insert_staging_data(
        df,
        truncate=truncate
    )

    return len(df)


# ==========================================================
# PROCESS CSV IN CHUNKS
# ==========================================================

def process_csv(file):

    total_rows = 0

    first_chunk = True

    chunk_number = 1

    for chunk in pd.read_csv(

        file,

        chunksize=10000,

        low_memory=False

    ):

        print(f"========== Chunk {chunk_number} ==========")

        rows = process_uploaded_dataframe(

            chunk,

            truncate=first_chunk

        )

        total_rows += rows

        first_chunk = False

        chunk_number += 1

        print(f"Inserted : {rows} rows")

        print(f"Total    : {total_rows}")

    return {

        "status": "success",

        "rows_processed": total_rows

    }


# ==========================================================
# PROCESS JSON
# ==========================================================

def process_json(data):

    df = pd.DataFrame(data)

    rows = process_uploaded_dataframe(

        df,

        truncate=True

    )

    return {

        "status": "success",

        "rows_processed": rows

    }