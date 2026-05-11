from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.item_routes import router as item_router
from routes.order_routes import router as order_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router)
app.include_router(item_router)
app.include_router(order_router)


@app.get("/")
def home():
    return {
        "message": "Canteen Backend Running Successfully"
    }