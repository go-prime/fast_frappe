import frappe
from fastapi import FastAPI
from fast_frappe.ctrl import init_frappe
from fast_frappe.controllers.menu_items import router as menu_items_router
from fast_frappe.controllers.recipes import router as recipes_router
from fast_frappe.controllers.orders import router as orders_router

app = FastAPI()

app.include_router(recipes_router)
app.include_router(menu_items_router)
app.include_router(orders_router)

@app.get("/")
def read_root():
    # Initialize Frappe
    init_frappe()
    
    # Retrieve available DocTypes and system settings
    available_doctypes = frappe.get_list("DocType", {"module": "restaurant"})
    settings = frappe.get_single("System Settings")
    
    return {
        "available_doctypes": available_doctypes,
        "settings": settings.as_dict(),
    }