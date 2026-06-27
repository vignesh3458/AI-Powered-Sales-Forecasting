import pandas as pd

from pathlib import Path





def load_dataset(file_path):


    file_path = Path(file_path)


    extension = file_path.suffix.lower()



    print(

        "Detected File Type:",

        extension

    )





    # ======================
    # CSV
    # ======================


    if extension == ".csv":


        df = pd.read_csv(

            file_path,

            low_memory=False

        )




    # ======================
    # JSON
    # ======================


    elif extension == ".json":


        try:


            df = pd.read_json(

                file_path

            )


        except:


            df = pd.read_json(

                file_path,

                lines=True

            )




    # ======================
    # EXCEL
    # ======================


    elif extension in [

        ".xlsx",

        ".xls"

    ]:


        df = pd.read_excel(

            file_path

        )




    # ======================
    # PARQUET
    # ======================


    elif extension == ".parquet":


        df = pd.read_parquet(

            file_path

        )




    else:


        raise ValueError(

            f"Unsupported file type: {extension}"

        )





    print(

        "Loaded Rows:",

        len(df)

    )


    print(

        "Columns:",

        df.columns.tolist()

    )



    return df