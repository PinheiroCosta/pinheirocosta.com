from fastapi import APIRouter
from pydantic import BaseModel
from app.services import string_ops

router = APIRouter()

class TextInput(BaseModel):
    text: str

@router.post("/reverse")
def reverse(input: TextInput):
    return {"result": string_ops.reverse(input.text)}

@router.post("/uppercase")
def uppercase(input: TextInput):
    return {"result": string_ops.uppercase(input.text)}

@router.post("/lowercase")
def uppercase(input: TextInput):
    return {"result": string_ops.lowercase(input.text)}

@router.post("/slugify")
def slugify(input: TextInput):
    return {"result": string_ops.slugify(input.text)}

@router.post("/uuid")
def generate_uuid():
    return {"result": string_ops.generate_uuid()}

