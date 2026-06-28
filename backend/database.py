import pandas as pd

from sqlalchemy import create_engine, text

from backend.config import DATABASE_URL


# ==========================================================
# DATABASE ENGINE
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    future=True
)


# ==========================================================
# GET SALES DATA
# ==========================================================

def get_sales_data():

    query = text("""
        SELECT *
        FROM restaurant_sales
        ORDER BY "Date"
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df


# ==========================================================
# INSERT INTO PRODUCTION TABLE
# ==========================================================

def insert_sales_data(df):

    df.to_sql(
        "restaurant_sales",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
    )

    return True


# ==========================================================
# INSERT INTO STAGING TABLE
# ==========================================================

def insert_staging_data(df, truncate=False):

    if truncate:

        with engine.begin() as connection:

            connection.execute(
                text(
                    """
                    TRUNCATE TABLE restaurant_sales_staging
                    """
                )
            )

    df.to_sql(

        "restaurant_sales_staging",

        engine,

        if_exists="append",

        index=False,

        chunksize=5000,

        method="multi"

    )

    return True
# ==========================================================
# APPROVE STAGING DATA
# ==========================================================

def approve_staging_data():

    with engine.begin() as connection:

        connection.execute(text("""
            INSERT INTO restaurant_sales
            SELECT *
            FROM restaurant_sales_staging
        """))

        connection.execute(text("""
            TRUNCATE TABLE restaurant_sales_staging
        """))

        connection.execute(text("""
            UPDATE model_updates
            SET last_updated = CURRENT_TIMESTAMP
            WHERE id = 1
        """))

    return True


# ==========================================================
# UPDATE MODEL TIME
# ==========================================================

def update_model_time():

    with engine.begin() as connection:

        connection.execute(text("""
            UPDATE model_updates
            SET last_updated = CURRENT_TIMESTAMP
            WHERE id = 1
        """))


# ==========================================================
# GET MODEL TIME
# ==========================================================

def get_model_update_time():

    with engine.connect() as connection:

        result = connection.execute(text("""
            SELECT last_updated
            FROM model_updates
            WHERE id = 1
        """))

        row = result.fetchone()

        if row:
            return row[0]

    return None

# ==========================================================
# CREATE BILL
# ==========================================================

def create_bill(connection, bill):

    result = connection.execute(
        text("""
            INSERT INTO restaurant_bills (

                bill_no,
                bill_date,
                customer_name,
                service_type,
                order_source,
                payment_method,
                table_no,
                no_of_pax,
                gross_sales,
                discount_amount,
                service_charge,
                tax_amount,
                delivery_charge,
                total_billed,
                tips,
                net_revenue

            )

            VALUES (

                :bill_no,
                :bill_date,
                :customer_name,
                :service_type,
                :order_source,
                :payment_method,
                :table_no,
                :no_of_pax,
                :gross_sales,
                :discount_amount,
                :service_charge,
                :tax_amount,
                :delivery_charge,
                :total_billed,
                :tips,
                :net_revenue

            )

            RETURNING bill_id
        """),
        bill
    )

    return result.scalar()
# ==========================================================
# ADD BILL ITEMS
# ==========================================================

def add_bill_items(connection, bill_id, items):

    query = text("""
        INSERT INTO restaurant_bill_items (

            bill_id,
            item_name,
            category,
            menu_group,
            quantity,
            item_rate,
            discount_amount,
            order_amount

        )

        VALUES (

            :bill_id,
            :item_name,
            :category,
            :menu_group,
            :quantity,
            :item_rate,
            :discount_amount,
            :order_amount

        )
    """)

    # If a single dictionary is passed, convert it to a list
    if isinstance(items, dict):
        items = [items]

    for item in items:

        # Support both Pydantic model and dict
        if hasattr(item, "model_dump"):
            item = item.model_dump()

        connection.execute(
            query,
            {
                "bill_id": bill_id,
                "item_name": item["item_name"],
                "category": item["category"],
                "menu_group": item["menu_group"],
                "quantity": item["quantity"],
                "item_rate": item["item_rate"],
                "discount_amount": item["discount_amount"],
                "order_amount": item["quantity"] * item["item_rate"]
            }
        )

    return True

# ==========================================================
# INSERT ANALYTICS RECORD
# ==========================================================

def insert_sales_record(connection, sales_record):

    columns = list(sales_record.keys())

    column_sql = ",".join(f'"{c}"' for c in columns)

    value_sql = ",".join(f":{c}" for c in columns)

    query = text(f"""
        INSERT INTO restaurant_sales
        ({column_sql})
        VALUES
        ({value_sql})
    """)

    connection.execute(query, sales_record)

    return True

# ==========================================================
# GET BILL
# ==========================================================

def get_bill(connection, bill_no):

    result = connection.execute(
        text("""
            SELECT *
            FROM restaurant_bills
            WHERE bill_no = :bill_no
        """),
        {
            "bill_no": bill_no
        }
    ).mappings().first()

    if result is None:
        return None

    return dict(result)
# ==========================================================
# UPDATE BILL
# ==========================================================

def update_bill(connection, bill_no, bill):

    connection.execute(
        text("""
            UPDATE restaurant_bills
            SET

                bill_date = :bill_date,
                service_type = :service_type,
                order_source = :order_source,
                payment_method = :payment_method,
                table_no = :table_no,
                no_of_pax = :no_of_pax,
                gross_sales = :gross_sales,
                discount_amount = :discount_amount,
                service_charge = :service_charge,
                tax_amount = :tax_amount,
                delivery_charge = :delivery_charge,
                total_billed = :total_billed,
                tips = :tips,
                net_revenue = :net_revenue

            WHERE bill_no = :bill_no
        """),
        {
            **bill,
            "bill_no": bill_no
        }
    )

    return True

# ==========================================================
# DELETE BILL ITEMS
# ==========================================================

def delete_bill_items(connection, bill_id):

    connection.execute(
        text("""
            DELETE
            FROM restaurant_bill_items
            WHERE bill_id = :bill_id
        """),
        {
            "bill_id": bill_id
        }
    )

    return True

# ==========================================================
# GET BILL ID
# ==========================================================

def get_bill_id(connection, bill_no):

    result = connection.execute(
        text("""
            SELECT bill_id
            FROM restaurant_bills
            WHERE bill_no = :bill_no
        """),
        {
            "bill_no": bill_no
        }
    ).fetchone()

    if result:
        return result[0]

    return None
# ==========================================================
# GET BILL ITEMS
# ==========================================================

def get_bill_items(connection, bill_no):

    result = connection.execute(
        text("""
            SELECT
                bi.item_name,
                bi.category,
                bi.menu_group,
                bi.quantity,
                bi.item_rate,
                bi.discount_amount
            FROM restaurant_bill_items bi
            JOIN restaurant_bills b
                ON bi.bill_id = b.bill_id
            WHERE b.bill_no = :bill_no
        """),
        {
            "bill_no": bill_no
        }
    )

    return [
        dict(row._mapping)
        for row in result
    ]

# ==========================================================
# DELETE ANALYTICS RECORDS
# ==========================================================

def delete_sales_records(connection, bill_no):

    connection.execute(
        text("""
            DELETE
            FROM restaurant_sales
            WHERE "BillNo" = :bill_no
        """),
        {
            "bill_no": bill_no
        }
    )

    return True

# ==========================================================
# SOFT DELETE BILL
# ==========================================================

def soft_delete_bill(connection, bill_no, deleted_by):

    connection.execute(
        text("""
            UPDATE restaurant_bills
            SET
                is_deleted = TRUE,
                deleted_at = CURRENT_TIMESTAMP,
                deleted_by = :deleted_by,
                updated_at = CURRENT_TIMESTAMP
            WHERE bill_no = :bill_no
              AND is_deleted = FALSE
        """),
        {
            "bill_no": bill_no,
            "deleted_by": deleted_by
        }
    )

    return True

# ==========================================================
# RESTORE BILL
# ==========================================================

def restore_bill(connection, bill_no):

    connection.execute(
        text("""
            UPDATE restaurant_bills
            SET
                is_deleted = FALSE,
                deleted_at = NULL,
                deleted_by = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE bill_no = :bill_no
        """),
        {
            "bill_no": bill_no
        }
    )

    return True