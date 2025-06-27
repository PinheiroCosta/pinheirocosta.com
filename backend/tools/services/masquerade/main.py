from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from random import randint
import tempfile
import os

from models import FichaVampiro
from generator import gerar_ficha_completa
from validator import validar_ficha


app = FastAPI(title="Gerador de Fichas - Vampiro: A Máscara", version="0.1.0")


class FichaRequest(BaseModel):
    geracao: Optional[int] = Field(default=None, ge=1, le=13)
    atributos: Optional[Dict[str, int]] = None
    habilidades: Optional[Dict[str, int]] = None
    antecedentes: Optional[Dict[str, int]] = None
    disciplinas: Optional[Dict[str, int]] = None
    virtudes: Optional[Dict[str, int]] = None
    nome: Optional[str] = None
    cla: Optional[str] = None
    conceito: Optional[str] = None
    comportamento: Optional[str] = None
    natureza: Optional[str] = None


@app.post("/fichas/vampiro")
async def criar_ficha(payload: FichaRequest):
    geracao = payload.geracao if payload.geracao is not None else randint(5, 13)
    data_dict = payload.model_dump(exclude_unset=True)
    data_dict["geracao"] = geracao

    ficha = gerar_ficha_completa(data_dict)
    validar_ficha(ficha)

    resposta = {
        "mensagem": "Ficha criada com sucesso!",
        "ficha": ficha.model_dump(),
    }

    return resposta


@app.get("/")
def status():
    return {"status": "ok", "msg": "Use POST /fichas/vampiro para gerar fichas."}
