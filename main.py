from fastapi import FastAPI
from .schemas import ProductSchema

app = FastAPI()

@app.get("/", tags=["status"])
def get_status():
  return {"message": "OK"}