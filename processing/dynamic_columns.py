from sqlalchemy import text





def get_sql_type(dtype):


    dtype = str(dtype)



    if "int" in dtype:


        return "INTEGER"



    elif "float" in dtype:


        return "DOUBLE PRECISION"



    elif "datetime" in dtype:


        return "TIMESTAMP"



    elif "bool" in dtype:


        return "BOOLEAN"



    else:


        return "TEXT"









def update_table_columns(
        engine,
        df,
        table_name="restaurant_sales"
):


    with engine.begin() as connection:



        # ==========================
        # EXISTING DB COLUMNS
        # ==========================


        result = connection.execute(

            text(

                """

                SELECT column_name

                FROM information_schema.columns

                WHERE table_name = :table

                """

            ),

            {

                "table":table_name

            }

        )



        existing_columns = [

            row[0]

            for row in result.fetchall()

        ]








        # ==========================
        # ADD NEW COLUMNS
        # ==========================


        for column in df.columns:



            if column not in existing_columns:



                sql_type = get_sql_type(

                    df[column].dtype

                )




                safe_column = (

                    column

                    .replace('"',"")

                )




                connection.execute(

                    text(

                        f'''

                        ALTER TABLE {table_name}

                        ADD COLUMN "{safe_column}"

                        {sql_type}

                        '''

                    )

                )