from fastapi import FastAPI

from app.routers import user

app = FastAPI()

# Includ Routes
app.include_router(user.router, prefix="/user")


@app.get("/")
async def root():
    return {"message": "Hello World"}