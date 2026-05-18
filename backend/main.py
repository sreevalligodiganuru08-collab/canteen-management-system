from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.item_routes import router as menu_router
from routes.cart_routes import router as cart_router
from routes.order_routes import router as order_router
from routes.dashboard_routes import router as dashboard_router


app = FastAPI(
    title="Canteen Management System API",
    version="1.0.0"
)


# =====================================
# CORS CONFIGURATION
# =====================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# ROOT ROUTE
# =====================================
@app.get("/")
def home():

    return {
        "message": "Canteen Management System API Running Successfully"
    }


# =====================================
# INCLUDE ROUTERS
# =====================================
app.include_router(auth_router)

app.include_router(menu_router)

app.include_router(cart_router)

app.include_router(order_router)

app.include_router(dashboard_router)