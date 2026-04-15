from fastapi import APIRouter

from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.profiles import router as profiles_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.orders import router as orders_router
from app.api.v1.endpoints.order_items import router as order_items_router
from app.api.v1.auth import router as auth_router
from app.api.v1.protected import router as protected_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(profiles_router)
api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(orders_router)
api_router.include_router(order_items_router)
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(protected_router, tags=["protected"])