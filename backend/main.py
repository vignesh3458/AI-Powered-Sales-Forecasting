from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Optional
import traceback
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth.auth_schema import LoginRequest
from backend.auth.auth_service import login_user
from backend.auth.dependencies import (
    get_current_user,
    require_roles
)
from fastapi import Depends
from backend.upload_service import (
    process_csv,
    process_json
)
from backend.sales_service import (
    create_sale,
    get_sale,
    update_sale,
    soft_delete_sale,
    restore_sale
)
from backend.schemas import CreateBill

from backend.database import (
    approve_staging_data
)

from backend.api_service import (
    sales_api,
    summary_api,
    monthly_api,
    category_api,
    payment_api,
    top_products_api
)

app = FastAPI(
    title="Restaurant Sales API",
    version="1.0.0"
)

# =====================================================
# LOGIN
# =====================================================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    result = login_user(
        form_data.username,
        form_data.password
    )

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return result
# =====================================================
# SALES
# =====================================================

@app.get("/sales")
def get_sales(limit: Optional[int] = None):

    return sales_api(limit)


# =====================================================
# SUMMARY
# =====================================================

@app.get("/summary")
def get_summary():

    return summary_api()


# =====================================================
# MONTHLY SALES
# =====================================================

@app.get("/monthly")
def get_monthly():

    return monthly_api()


# =====================================================
# CATEGORY SALES
# =====================================================

@app.get("/category")
def get_category():

    return category_api()


# =====================================================
# PAYMENT SUMMARY
# =====================================================

@app.get("/payment")
def get_payment():

    return payment_api()


# =====================================================
# TOP PRODUCTS
# =====================================================

@app.get("/top-products")
def get_top_products():

    return top_products_api()


# =====================================================
# UPLOAD CSV
# =====================================================

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    try:

        return process_csv(file.file)

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# UPLOAD JSON
# =====================================================

@app.post("/upload-json")
async def upload_json(data: list):

    try:

        return process_json(data)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# APPROVE DATA
# =====================================================

@app.post("/approve")
def approve():

    try:

        approve_staging_data()

        return {

            "status": "success",

            "message": "Dataset approved successfully."

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =====================================================
# CREATE SALE
# =====================================================

from fastapi import Depends
from backend.auth.dependencies import get_current_user

@app.post("/sales")
def create_new_sale(
    bill: CreateBill,
    current_user: dict = Depends(
        require_roles(
            "Admin",
            "Manager",
            "Cashier"
        )
    )
):

    try:

        return create_sale(bill)

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
# =====================================================
# GET BILL
# =====================================================

@app.get("/sales/{bill_no}")

def get_bill_by_number(bill_no: int):

    try:

        return get_sale(bill_no)

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
# =====================================================
# UPDATE BILL
# =====================================================

@app.put("/sales/{bill_no}")
def update_bill_api(bill_no: int, bill: CreateBill):

    try:

        return update_sale(
            bill_no,
            bill.model_dump()
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():

    return {

        "project": "Restaurant Sales Forecast API",

        "status": "Running"

    }

# =====================================================
# DELETE BILL (SOFT DELETE)
# =====================================================

@app.delete("/sales/{bill_no}")
def delete_sale(
    bill_no: int,
    current_user: dict = Depends(
        require_roles(
            "Admin",
            "Manager"
        )
    )
):

    try:

        return soft_delete_sale(
            bill_no,
            current_user["username"]
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
# =====================================================
# RESTORE BILL
# =====================================================

@app.post("/sales/{bill_no}/restore")
def restore_deleted_sale(
    bill_no: int,
    current_user: dict = Depends(
        require_roles(
            "Admin",
            "Manager"
        )
    )
):

    try:

        return restore_sale(
            bill_no
        )

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )