from fastapi.responses import JSONResponse
from fastapi import APIRouter

from fast_frappe.ctrl import init_frappe
from restaurant.public_api import get_orders as fetch_orders


router = APIRouter()


@router.get('/get_orders/{server_id}')
def get_orders(server_id: str):
    """
    Retrieve an orders filtered per Server.

    - **server_id**: The ID of the server with which to filter orders to retrieve.
    """
    init_frappe()
    data = fetch_orders(server_id=server_id)
    return JSONResponse(content=data)