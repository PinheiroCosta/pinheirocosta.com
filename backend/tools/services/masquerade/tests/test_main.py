import asyncio
import time
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_criar_ficha_valida():
    payload = {
        "geracao": 10,
        "atributos": {"força": 5, "destreza": 5, "vigor": 5},
        "habilidades": {},
        "disciplinas": {},
        "nome": "Teste",
        "cla": "Toreador",
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/fichas/vampiro", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert "problemas" in body["detail"]
    assert any("excedem o limite" in p for p in body["detail"]["problemas"])


@pytest.mark.asyncio
async def test_criar_ficha_aleatoria():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/fichas/vampiro", json={})

    assert response.status_code == 200
    body = response.json()
    assert "ficha" in body
    assert body["ficha"]["geracao"] >= 5
    assert sum(body["ficha"]["atributos"].values()) == 15
    assert sum(body["ficha"]["habilidades"].values()) == 27
    assert sum(body["ficha"]["disciplinas"].values()) == 3


@pytest.mark.asyncio
async def test_geracao_fora_limite():
    """Testes de Validação de Dados"""
    payload = {
        "geracao": 0,  # Fora do limite inferior
        "atributos": {"força": 5, "destreza": 5, "vigor": 5},
        "habilidades": {},
        "disciplinas": {},
        "nome": "Teste",
        "cla": "Toreador",
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/fichas/vampiro", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert "geracao" in body["detail"][0]["loc"]


@pytest.mark.asyncio
async def test_desempenho_criar_ficha_aleatoria():
    """Testes de Desempenho"""
    start_time = time.time()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/fichas/vampiro", json={})

    end_time = time.time()
    assert response.status_code == 200
    assert end_time - start_time < 1  # O tempo de resposta não pode exceder 1 segundo


@pytest.mark.asyncio
async def test_concorrencia_criar_ficha_aleatoria():
    """Testes de Concurrency"""

    async def fazer_requisicao():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/fichas/vampiro", json={})
        assert response.status_code == 200

    tasks = [fazer_requisicao() for _ in range(10)]  # 10 requisições simultâneas
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_estrutura_resposta():
    """Testes de Resposta Completa"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/fichas/vampiro", json={})

    assert response.status_code == 200
    body = response.json()
    assert "ficha" in body
    assert "geracao" in body["ficha"]
    assert "atributos" in body["ficha"]
    assert "habilidades" in body["ficha"]
    assert "disciplinas" in body["ficha"]
