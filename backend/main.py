from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =====================================
# ROUTERS IMPORTS
# =====================================
from routes.auth_routes import router as auth_router

from routes.item_routes import router as item_router

from routes.cart_routes import router as cart_router

from routes.order_routes import router as order_router

from routes.payment_routes import router as payment_router

from routes.delivery_routes import router as delivery_router

from routes.notification_routes import router as notification_router

from routes.dashboard_routes import router as dashboard_router

from routes.analytics_routes import router as analytics_router

from routes.offer_routes import router as offer_router

from routes.combo_routes import router as combo_router


# =====================================
# FASTAPI APP
# =====================================
app = FastAPI(

    title="Canteen Management System API",

    version="2.0.0"
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

        "message": "Canteen Management System API Running Successfully",

        "version": "2.0.0",

        "status": "Server Active"
    }


# =====================================
# INCLUDE ROUTERS
# =====================================

# AUTH
app.include_router(auth_router)

# ITEMS
app.include_router(item_router)

# CART
app.include_router(cart_router)

# ORDERS
app.include_router(order_router)

# PAYMENTS
app.include_router(payment_router)

# DELIVERY
app.include_router(delivery_router)

# NOTIFICATIONS
app.include_router(notification_router)

# DASHBOARD
app.include_router(dashboard_router)

# ANALYTICS
app.include_router(analytics_router)

# OFFERS
app.include_router(offer_router)

# COMBOS
app.include_router(combo_router)