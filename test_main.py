import pytest
from fastapi.testclient import TestClient

from main import app, fila_clientes


client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_fila_antes_de_cada_teste():
    fila_clientes.clear()
    yield
    fila_clientes.clear()


def adicionar(nome: str, tipo: str = "N"):
    return client.post("/fila", json={"nome": nome, "tipo": tipo})


def test_fila_vazia_retorna_lista_vazia_e_status_200():
    resposta = client.get("/fila")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_adiciona_cliente_normal_no_final_da_fila():
    resposta = adicionar("Mariana", "N")
    dados = resposta.json()

    assert resposta.status_code == 201
    assert dados["nome"] == "Mariana"
    assert dados["tipo"] == "N"
    assert dados["posicao"] == 1
    assert dados["atendido"] is False
    assert dados["data_chegada"]


def test_prioridade_fica_antes_dos_clientes_normais():
    adicionar("Ana", "N")
    adicionar("Bruno", "N")
    adicionar("Carla", "P")
    adicionar("Davi", "P")

    fila = client.get("/fila").json()
    assert [pessoa["nome"] for pessoa in fila] == [
        "Carla",
        "Davi",
        "Ana",
        "Bruno",
    ]
    assert [pessoa["posicao"] for pessoa in fila] == [1, 2, 3, 4]


def test_consulta_cliente_pela_posicao():
    adicionar("Lívia", "N")
    resposta = client.get("/fila/1")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Lívia"


def test_consulta_posicao_inexistente_retorna_404():
    resposta = client.get("/fila/8")

    assert resposta.status_code == 404
    assert resposta.json() == {
        "detail": "Não existe cliente aguardando na posição 8."
    }


def test_put_atende_primeiro_e_atualiza_as_posicoes():
    adicionar("Carla", "P")
    adicionar("Ana", "N")
    adicionar("Bruno", "N")

    resposta = client.put("/fila")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["cliente_atendido"]["nome"] == "Carla"
    assert dados["cliente_atendido"]["posicao"] == 0
    assert dados["cliente_atendido"]["atendido"] is True
    assert [pessoa["posicao"] for pessoa in dados["fila_atualizada"]] == [1, 2]


def test_delete_remove_cliente_e_fecha_espaco_na_fila():
    adicionar("Ana", "N")
    adicionar("Bruno", "N")
    adicionar("Carlos", "N")

    resposta = client.delete("/fila/2")
    fila = resposta.json()["fila_atualizada"]

    assert resposta.status_code == 200
    assert [pessoa["nome"] for pessoa in fila] == ["Ana", "Carlos"]
    assert [pessoa["posicao"] for pessoa in fila] == [1, 2]


def test_delete_posicao_inexistente_retorna_404():
    resposta = client.delete("/fila/99")

    assert resposta.status_code == 404
    assert "posição 99" in resposta.json()["detail"]


@pytest.mark.parametrize(
    "dados",
    [
        {"nome": "", "tipo": "N"},
        {"nome": "Nome com mais de vinte caracteres", "tipo": "N"},
        {"nome": "João", "tipo": "X"},
        {"nome": "João", "tipo": "Normal"},
    ],
)
def test_dados_invalidos_retornam_422(dados):
    resposta = client.post("/fila", json=dados)
    assert resposta.status_code == 422

