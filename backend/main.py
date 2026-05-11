from fastapi import FastAPI

app = FastAPI(
    title="Canteen Management System",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Canteen Backend Running Successfully"
    }