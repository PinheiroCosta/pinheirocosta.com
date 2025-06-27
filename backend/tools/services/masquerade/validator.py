from fastapi import HTTPException
from models import FichaVampiro


def validar_ficha(ficha: FichaVampiro):
    erros = []
    # Validação de Geracao
    if ficha.geracao < 1 or ficha.geracao > 13:
        erros.append("Geração deve estar num intervalo entre 1 e 13")

    # Validação de Atributos
    if any(v < 1 for v in ficha.atributos.values()):
        erros.append("Todos os atributos devem ter pelo menos 1 ponto.")
    if sum(ficha.atributos.values()) > 15:
        erros.append("Atributos excedem o limite permitido (15).")

    # Validação de habilidades
    if sum(ficha.habilidades.values()) > 27:
        erros.append("Habilidades excedem o limite permitido (27)gt.")

    # Validação de disciplinas
    if sum(ficha.disciplinas.values()) > 3:
        erros.append("Disciplinas excedem o limite permitido (3).")

    if erros:
        raise HTTPException(
            status_code=422,
            detail={
                "erro": "validacao_regra_negocio",
                "mensagem": "A ficha enviada possui erros de distribuição de pontos.",
                "problemas": erros,
            },
        )
