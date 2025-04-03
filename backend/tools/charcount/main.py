from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Character Counter API")

class TextInput(BaseModel):
    text: str

@app.post("/count/")
def count_characters(data: TextInput):
    char_count = len(data.text)
    word_count = len(data.text.split())
    return {"characters": char_count, "words": word_count}

