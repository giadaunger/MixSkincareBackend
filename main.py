from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["status"])
def get_status():
  return {"message": "OK"}