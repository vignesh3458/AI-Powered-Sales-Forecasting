from pydantic import BaseModel

from typing import Optional

from datetime import datetime





class SalesData(BaseModel):


    # ==========================
    # DATE
    # ==========================

    Date: datetime





    # ==========================
    # BILL DETAILS
    # ==========================

    BillNo: Optional[str] = None





    # ==========================
    # PRODUCT DETAILS
    # ==========================

    Category: Optional[str] = None


    Item_Name: Optional[str] = None


    Quantity: Optional[int] = 0


    Unit_Price: Optional[float] = 0





    # ==========================
    # REVENUE DETAILS
    # ==========================

    Total_Billed: float


    Discount_Amt: Optional[float] = 0


    Service_Charge: Optional[float] = 0


    Delivery_Charge: Optional[float] = 0





    # ==========================
    # TAX DETAILS
    # ==========================

    CGST: Optional[float] = 0


    SGST: Optional[float] = 0


    TotalTaxAmount: Optional[float] = 0





    # ==========================
    # FINAL FORECAST TARGET
    # ==========================

    Net_Revenue: Optional[float] = 0





    # ==========================
    # CUSTOMER / BUSINESS
    # ==========================

    Payment_Method: Optional[str] = None


    Weather: Optional[str] = None





    # ==========================
    # FORECAST FEATURES
    # ==========================

    Is_Holiday: Optional[int] = 0


    Is_Weekend: Optional[int] = 0


    Promotion_Flag: Optional[int] = 0


    Festival_Flag: Optional[int] = 0


    Weather_Index: Optional[float] = 0

# ==========================================================
# RESTAURANT POS SCHEMAS
# ==========================================================

from typing import List


class BillItem(BaseModel):

    item_name: str

    category: str

    menu_group: str

    quantity: int

    item_rate: float

    discount_amount: float = 0


class CreateBill(BaseModel):

    bill_no: int

    bill_date: datetime

    customer_name: str = "Walk-in"

    service_type: str

    order_source: str

    payment_method: str

    table_no: str

    no_of_pax: int

    gross_sales: float

    discount_amount: float

    service_charge: float

    tax_amount: float

    delivery_charge: float

    total_billed: float

    tips: float

    net_revenue: float

    items: List[BillItem]


class UpdateBill(BaseModel):

    payment_method: Optional[str] = None

    table_no: Optional[str] = None

    no_of_pax: Optional[int] = None

    gross_sales: Optional[float] = None

    discount_amount: Optional[float] = None

    service_charge: Optional[float] = None

    tax_amount: Optional[float] = None

    delivery_charge: Optional[float] = None

    total_billed: Optional[float] = None

    tips: Optional[float] = None

    net_revenue: Optional[float] = None


class BillResponse(BaseModel):

    bill_no: int

    message: str

    created_at: datetime