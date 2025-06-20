from fastapi import FastAPI
from app.api.v1 import endpoints


app = FastAPI(title="StringUtils API", version="0.1.0")

app.include_router(endpoints.router, prefix="/api/v1/stringutils", tags=["stringutils"])
