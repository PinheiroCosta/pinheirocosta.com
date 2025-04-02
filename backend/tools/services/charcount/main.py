from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Character Counter API")

ESCAPED_CHARS = {"\n", "\t", "\r", "\b", "\f", "\\", "\v"}

class TextInput(BaseModel):
    text: str
    count_spaces: bool = True
    count_special: bool = True
    count_escaped: bool = True

@app.post("/count/")
def count_characters(data: TextInput):
    text = bytes(data.text, "utf-8").decode("unicode_escape")  # ← aqui
    escaped_chars = {"\n", "\t", "\r", "\f", "\v"}
    filtered = []

    for ch in text:
        if ch in escaped_chars:
            if data.count_escaped:
                filtered.append(ch)
            continue

        if ch.isspace():
            if data.count_spaces:
                filtered.append(ch)
            continue

        if not ch.isalnum():
            if data.count_special:
                filtered.append(ch)
            continue

        # alfanuméricos sempre entram
        filtered.append(ch)

    return {
        "characters": len(filtered),
        "words": len("".join(filtered).split()),
    }

