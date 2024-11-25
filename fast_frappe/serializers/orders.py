from pydantic import BaseModel, Field, validator
from typing import List, Optional

class OrderItem(BaseModel):
    menu_item: str = Field(..., alias="menu_item", description="The name of the menu item ordered")
    description: Optional[str] = Field(None, alias="description", description="The description of the menu item ordered")
    special_instructions: Optional[str] = Field(None, alias="special_instructions", description="Any special instructions for the order")
    qty: int = Field(..., alias="qty", gt=0, description="The quantity of the menu item ordered")
    unit_price: float = Field(..., ge=0, alias="unit_price", description="The unit price of the menu item ordered")
    discount: Optional[float] = Field(None, alias="discount", description="The discount applied to the menu item ordered")
    tax_rate: Optional[float] = Field(None, alias="tax_rate", description="The tax rate applied to the menu item ordered")
    tax_amount: Optional[float] = Field(None, alias="tax_amount", description="The tax amount applied to the menu item ordered")
    amount: float = Field(..., alias="amount", ge=0, description="The total amount of the menu item ordered")
    
    @validator('qty')
    def validate_qty(cls, qty, values):
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero")
        return qty


class Order(BaseModel):
    table: str = Field(..., alias="table", description="The table number for the order")
    status: str = Field(..., alias="status", description="The status of the order", pattern="^(Ordered|Served)$")
    currency: str = Field(..., alias="currency", description="The currency of the order")
    date: Optional[str] = Field(None, alias="date", description="The date of the order")
    time: Optional[str] = Field(None, alias="time", description="The time of the order")   
    items: List[OrderItem] = Field(..., alias="items", description="The items in the order")
    subtotal: float = Field(..., alias="subtotal", description="The subtotal of the order")
    tax: float = Field(..., alias="tax", description="The tax of the order")
    total: float = Field(..., alias="total", description="The total of the order")
    server: Optional[str] = Field(..., alias="server", description="The server who took the order")
    payment_status: str = Field(..., alias="payment_status", description="The payment status of the order", pattern="^(Ordered|Paid|Refunded)$")
    source_warehouse: Optional[str] = Field(None, alias="source_warehouse", description="The source warehouse for the order")
    
    # Validations
    @validator('total')
    def validate_total(cls, total, values):
        items = values.get('items', [])
        calculated_total = sum(item.amount for item in items)
        if total != calculated_total:
            raise ValueError(f"Total does not match the sum of item amounts ({calculated_total})")
        return total
