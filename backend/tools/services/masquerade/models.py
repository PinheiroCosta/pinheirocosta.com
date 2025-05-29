from pydantic import BaseModel, Field, ConfigDict
from typing import Dict


class FichaVampiro(BaseModel):
    nome: str
    cla: str
    humanidade: int
    vontade: int
    geracao: int = Field(..., ge=1, le=13, description="Geração entre 1 (Caim) e 13 (neófitos)")
    atributos: Dict[str, int] = Field(..., description="Ex: força, destreza, vigor")
    habilidades: Dict[str, int] = Field(..., description="Ex: empatia, expressão")
    disciplinas: Dict[str, int] = Field(..., description="Ex: presença, ofuscação")
    antecedentes: Dict[str, int] = Field(..., description="Ex: Status, Lacaios, Rebanho")
    virtudes: Dict[str, int] = Field(..., description="Ex: consciencia, autocontrole")
    conceito: str
    conceito_descricao: str
    comportamento: str
    comportamento_descricao: str
    natureza: str
    natureza_descricao: str

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "nome": "Lucien",
                "cla": "Toreador",
                "conceito": "artista",
                "geracao": 10,
                "atributos": {
                    "forca": 2,
                    "destreza": 3,
                    "vigor": 2
                },
                "habilidades": {
                    "empatia": 2,
                    "expressao": 3
                },
                "disciplinas": {
                    "presenca": 2
                },
                "antecedentes": {
                    "lacaios": 1,
                    "fama": 2
                },
                "virtudes": {
                    "consciência": 1,
                    "autocontrole": 1,
                    "coragem": 1
                },
                "humanidade": 2,
                "vontade": 1, 
            }
        }
    )

