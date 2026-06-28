from backend.database import (
    engine,

    # Create
    create_bill,
    add_bill_items,
    insert_sales_record,

    # Read
    get_bill,
    get_bill_id,

    # Update
    update_bill,

    # Delete
    delete_bill_items,
    soft_delete_bill,
    delete_sales_records,
    restore_bill,
    get_bill_items,
)

from processing.sales_transformer import (
    transform_bill_to_sales
)

# ==========================================================
# CREATE COMPLETE SALE
# ==========================================================

def create_sale(bill):

    with engine.begin() as connection:

        bill_data = {

            "bill_no": bill.bill_no,

            "bill_date": bill.bill_date,

            "customer_name": bill.customer_name,

            "service_type": bill.service_type,

            "order_source": bill.order_source,

            "payment_method": bill.payment_method,

            "table_no": bill.table_no,

            "no_of_pax": bill.no_of_pax,

            "gross_sales": bill.gross_sales,

            "discount_amount": bill.discount_amount,

            "service_charge": bill.service_charge,

            "tax_amount": bill.tax_amount,

            "delivery_charge": bill.delivery_charge,

            "total_billed": bill.total_billed,

            "tips": bill.tips,

            "net_revenue": bill.net_revenue

        }

        bill_id = create_bill(connection, bill_data)

        add_bill_items(
            connection,
            bill_id,
            bill.items
        )

        for item in bill.items:

            sales_record = transform_bill_to_sales(

                bill_data,

                item.model_dump()

            )

            insert_sales_record(
                connection,
                sales_record
            )

    return {

        "message": "Bill created successfully",

        "bill_no": bill.bill_no

    }

# ==========================================================
# GET COMPLETE SALE
# ==========================================================

def get_sale(bill_no: int):

    with engine.connect() as connection:

        result = get_bill(
            connection,
            bill_no
        )

        if result is None:

            return {
                "message": "Bill not found"
            }

        return result
    
# ==========================================================
# UPDATE SALE
# ==========================================================

def update_sale(bill_no: int, bill_data: dict):

    with engine.begin() as connection:

        bill_id = get_bill_id(connection, bill_no)

        if bill_id is None:

            return {
                "message": "Bill not found"
            }

        # Update bill header
        update_bill(
            connection,
            bill_no,
            bill_data
        )

        # Delete existing bill items
        delete_bill_items(
            connection,
            bill_id
        )

        # Delete existing analytics
        delete_sales_records(
            connection,
            bill_no
        )

        # Insert new bill items
        for item in bill_data["items"]:

            add_bill_items(
                connection,
                bill_id,
                item
            )

            analytics = transform_bill_to_sales(
                bill_data,
                item
            )

            insert_sales_record(
                connection,
                analytics
            )

        return {
            "message": "Bill updated successfully",
            "bill_no": bill_no
        }
    
# ==========================================================
# SOFT DELETE SALE
# ==========================================================

def soft_delete_sale(
    bill_no: int,
    deleted_by: str
):

    with engine.begin() as connection:

        soft_delete_bill(
            connection,
            bill_no,
            deleted_by
        )

        delete_sales_records(
            connection,
            bill_no
        )

        return {
            "message": "Bill deleted successfully",
            "bill_no": bill_no
        }
    
    # ==========================================================
# RESTORE SALE
# ==========================================================

def restore_sale(bill_no: int):

    with engine.begin() as connection:

        restore_bill(
            connection,
            bill_no
        )

        bill = get_bill(
            connection,
            bill_no
        )

        items = get_bill_items(
            connection,
            bill_no
        )
        for item in items:

            analytics = transform_bill_to_sales(
                bill,
                item
            )

            insert_sales_record(
                connection,
                analytics
            )

        return {
            "message": "Bill restored successfully",
            "bill_no": bill_no
        }