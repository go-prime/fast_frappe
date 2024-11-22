from fastapi.responses import JSONResponse
from fastapi import APIRouter

from fast_frappe.ctrl import init_frappe
from restaurant.public_api import get_recipes as fetch_recipies


router = APIRouter()


@router.get('/get_recipes/')
def recipes():
    init_frappe()
    data = fetch_recipies()
    return JSONResponse(content=data)


@router.get('/get_recipes/{recipe_id}')
def recipe(recipe_id: str):
    """
    Retrieve an recipe by its ID.

    - **recipe_id**: The ID of the item to retrieve.
    """
    init_frappe()
    data = fetch_recipies(recipe=recipe_id)
    return JSONResponse(content=data)
