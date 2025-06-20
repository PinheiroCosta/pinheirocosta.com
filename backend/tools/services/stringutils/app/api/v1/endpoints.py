from fastapi import APIRouter
from app.services import string_ops
from app.schemas import TextInput, CharCountInput

router = APIRouter()


@router.post("/reverse")
def reverse(input: TextInput):
    return {"result": string_ops.reverse(input.text)}

@router.post("/uppercase")
def uppercase(input: TextInput):
    return {"result": string_ops.uppercase(input.text)}

@router.post("/lowercase")
def lowercase(input: TextInput):
    return {"result": string_ops.lowercase(input.text)}

@router.post("/slugify")
def slugify(input: TextInput):
    return {"result": string_ops.slugify(input.text)}

@router.post("/uuid")
def generate_uuid():
    return {"result": string_ops.generate_uuid()}

@router.post("/charcount")
def count(input: CharCountInput):
    return string_ops.count_characters(
        text=input.text,
        count_spaces=input.count_spaces,
        count_special=input.count_special,
        count_escaped=input.count_escaped,
    )

@router.post("/ascii")
def ascii_converter(input: TextInput):
    return {"result": string_ops.ascii_converter(input.text)}

@router.post("/palindrome")
def palindrome(input: TextInput):
    return {"result": string_ops.is_palindrome(input.text)}
