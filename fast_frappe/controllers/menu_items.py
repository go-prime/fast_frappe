# controllers/menu_items.py

from fastapi.responses import JSONResponse
from fastapi import APIRouter

from fast_frappe.ctrl import init_frappe
from restaurant.public_api import get_menu_items


router = APIRouter()

@router.get('/get_menu_items/')
def menu_items():
    init_frappe()
    data = get_menu_items()
    return JSONResponse(content=data)