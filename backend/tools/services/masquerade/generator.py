from random import choices, randint, sample
from typing import Optional, Dict
from models import FichaVampiro
from constants import (
    ATRIBUTOS_PONTOS_INICIAIS, HABILIDADES_PONTOS_INICIAIS, DISCIPLINAS_PONTOS_INICIAIS, ANTECEDENTES_PONTOS_INICIAIS,
    VIRTUDES_PONTOS_INICIAIS, ATRIBUTOS_POSSIVEIS, HABILIDADES_POSSIVEIS, DISCIPLINAS_POSSIVEIS, CLAS_POSSIVEIS,  
    ANTECEDENTES_POSSIVEIS, VIRTUDES_POSSIVEIS, CONCEITOS_POSSIVEIS, ARQUETIPOS_POSSIVEIS 
)


def gerar_distribuicao_com_base(
    possiveis: list[str], 
    total: int, 
    fornecido: Optional[Dict[str, int]] = None,
    minimo_por_item: int = 0,
    remove_zeros: bool = True
) -> dict[str, int]:

    fornecido = fornecido or {}
    
    # começa com o mínimo garantido
    distribuicao = {}
    for chave in possiveis:
        distribuicao[chave] = max(fornecido.get(chave, minimo_por_item), minimo_por_item)

    pontos_usados = sum(distribuicao.values())
    restante = total - pontos_usados
    
    if restante > 0:
        for _ in range(restante):
            escolha = choices(possiveis, k=1)[0]
            distribuicao[escolha] += 1
    
    if remove_zeros:
        distribuicao_sem_zerados = {chave: valor for chave, valor in distribuicao.items() if valor}
        return distribuicao_sem_zerados

    return distribuicao


def gerar_ficha_completa(data: dict) -> FichaVampiro:
    nome = data.get("nome", "NPC Gerado")
    cla = data.get("cla", choices(CLAS_POSSIVEIS, k=1)[0])
    geracao = data["geracao"]

    atributos_input = data.get("atributos", {})
    habilidades_input = data.get("habilidades", {})
    disciplinas_input = data.get("disciplinas", {})
    antecedentes_input = data.get("antecedentes", {})
    virtudes_input = data.get("virtudes", {})
    conceito_input = data.get("conceito")
    natureza_input = data.get("natureza")
    comportamento_input = data.get("comportamento")

    atributos = gerar_distribuicao_com_base(
        ATRIBUTOS_POSSIVEIS, ATRIBUTOS_PONTOS_INICIAIS, atributos_input, minimo_por_item=1
    )
    habilidades = gerar_distribuicao_com_base(
        HABILIDADES_POSSIVEIS, HABILIDADES_PONTOS_INICIAIS, habilidades_input
    )
    disciplinas = gerar_distribuicao_com_base(
        DISCIPLINAS_POSSIVEIS, DISCIPLINAS_PONTOS_INICIAIS, disciplinas_input
    )
    antecedentes = gerar_distribuicao_com_base(
        ANTECEDENTES_POSSIVEIS, ANTECEDENTES_PONTOS_INICIAIS, antecedentes_input
    )
    virtudes = gerar_distribuicao_com_base(
        VIRTUDES_POSSIVEIS, VIRTUDES_PONTOS_INICIAIS, virtudes_input, minimo_por_item=1
    )

    humanidade = virtudes.get("consciência", 0) + virtudes.get("autocontrole", 0)
    vontade = virtudes.get("coragem", 0)

    if conceito_input in CONCEITOS_POSSIVEIS:
        conceito = conceito_input
        conceito_descricao = CONCEITOS_POSSIVEIS[conceito_input]
    else:
        conceito_nome = choices(list(CONCEITOS_POSSIVEIS.keys()), k=1)[0]
        conceito = conceito_nome 
        conceito_descricao = CONCEITOS_POSSIVEIS[conceito_nome]

    if natureza_input in ARQUETIPOS_POSSIVEIS:
        natureza = natureza_input
        natureza_descricao = ARQUETIPOS_POSSIVEIS[natureza_input]
    else:
        natureza_nome = choices(list(ARQUETIPOS_POSSIVEIS.keys()), k=1)[0] 
        natureza = natureza_nome
        natureza_descricao = ARQUETIPOS_POSSIVEIS[natureza_nome]
        
    if comportamento_input in ARQUETIPOS_POSSIVEIS:
        comportamento = comportamento_input
        comportamento_descricao = ARQUETIPOS_POSSIVEIS[comportamento_input]
    else:
        comportamento_nome = choices(list(ARQUETIPOS_POSSIVEIS.keys()), k=1)[0] 
        comportamento = comportamento_nome
        comportamento_descricao = ARQUETIPOS_POSSIVEIS[comportamento_nome]

    ficha = FichaVampiro(
        nome=nome,
        cla=cla,
        geracao=geracao,
        atributos=atributos,
        habilidades=habilidades,
        disciplinas=disciplinas,
        antecedentes=antecedentes,
        virtudes=virtudes,
        humanidade=humanidade,
        vontade=vontade,
        conceito=conceito,
        conceito_descricao=conceito_descricao,
        natureza=natureza,
        natureza_descricao=natureza_descricao,
        comportamento=comportamento,
        comportamento_descricao=comportamento_descricao
    )

    return ficha 
