from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="API da Fila de Atendimento da Anna",
    description=(
        "API REST desenvolvida para controlar a fila presencial de um "
        "estabelecimento, com atendimentos normais e prioritários."
    ),
    version="1.0.0",
)

FUSO_BRASIL = timezone(timedelta(hours=-3), name="America/Sao_Paulo")


class NovoCliente(BaseModel):
    """Dados recebidos para colocar uma pessoa na fila."""

    nome: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Nome obrigatório com no máximo 20 caracteres",
        examples=["Maria"],
    )
    tipo: Literal["N", "P"] = Field(
        ...,
        description="N para atendimento normal ou P para prioritário",
        examples=["N"],
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, nome: str) -> str:
        nome_limpo = nome.strip()
        if not nome_limpo:
            raise ValueError("O nome não pode ficar vazio.")
        return nome_limpo


class ClienteFila(BaseModel):
    """Registro completo utilizado pela API."""

    posicao: int
    nome: str
    data_chegada: datetime
    tipo: Literal["N", "P"]
    atendido: bool


# A lista representa a fila enquanto a aplicação está em execução.
fila_clientes: list[ClienteFila] = []


def clientes_aguardando() -> list[ClienteFila]:
    """Retorna apenas quem ainda espera atendimento, em ordem de posição."""

    return sorted(
        (cliente for cliente in fila_clientes if not cliente.atendido),
        key=lambda cliente: cliente.posicao,
    )


def localizar_por_posicao(posicao: int) -> ClienteFila | None:
    """Localiza uma pessoa não atendida pela posição atual na fila."""

    return next(
        (
            cliente
            for cliente in fila_clientes
            if not cliente.atendido and cliente.posicao == posicao
        ),
        None,
    )


def reorganizar_apos_remocao(posicao_removida: int) -> None:
    """Fecha o espaço deixado por uma remoção na fila."""

    for cliente in fila_clientes:
        if not cliente.atendido and cliente.posicao > posicao_removida:
            cliente.posicao -= 1


@app.get("/", tags=["Informações"])
def inicio() -> dict:
    return {
        "api": "Fila de Atendimento",
        "aluna": "Anna Julia Torres Martins de Deus",
        "documentacao": "/docs",
        "status": "API em execução",
    }


@app.get(
    "/fila",
    response_model=list[ClienteFila],
    status_code=status.HTTP_200_OK,
    tags=["Fila"],
)
def listar_fila() -> list[ClienteFila]:
    """Lista as pessoas que ainda não foram atendidas."""

    return clientes_aguardando()


@app.get(
    "/fila/{posicao}",
    response_model=ClienteFila,
    status_code=status.HTTP_200_OK,
    tags=["Fila"],
)
def consultar_posicao(
    posicao: int = Path(..., ge=1, description="Posição procurada na fila"),
) -> ClienteFila:
    """Consulta a pessoa que ocupa uma posição específica."""

    cliente = localizar_por_posicao(posicao)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe cliente aguardando na posição {posicao}.",
        )
    return cliente


@app.post(
    "/fila",
    response_model=ClienteFila,
    status_code=status.HTTP_201_CREATED,
    tags=["Fila"],
)
def adicionar_cliente(novo_cliente: NovoCliente) -> ClienteFila:
    """Adiciona um cliente e calcula sua posição conforme a prioridade."""

    aguardando = clientes_aguardando()

    if novo_cliente.tipo == "P":
        # A nova prioridade fica depois das prioridades que já aguardam.
        quantidade_prioritarios = sum(
            1 for cliente in aguardando if cliente.tipo == "P"
        )
        nova_posicao = quantidade_prioritarios + 1

        # Clientes normais são deslocados uma posição para trás.
        for cliente in aguardando:
            if cliente.posicao >= nova_posicao:
                cliente.posicao += 1
    else:
        # O atendimento normal entra no fim da fila.
        nova_posicao = len(aguardando) + 1

    cliente = ClienteFila(
        posicao=nova_posicao,
        nome=novo_cliente.nome,
        data_chegada=datetime.now(FUSO_BRASIL),
        tipo=novo_cliente.tipo,
        atendido=False,
    )
    fila_clientes.append(cliente)
    return cliente


@app.put(
    "/fila",
    status_code=status.HTTP_200_OK,
    tags=["Fila"],
)
def chamar_proximo_cliente() -> dict:
    """Atende a posição 1 e adianta as outras pessoas em uma posição."""

    primeiro = localizar_por_posicao(1)
    if primeiro is None:
        return {
            "mensagem": "A fila está vazia. Nenhum cliente foi chamado.",
            "cliente_atendido": None,
            "fila_atualizada": [],
        }

    primeiro.posicao = 0
    primeiro.atendido = True

    for cliente in fila_clientes:
        if not cliente.atendido:
            cliente.posicao -= 1

    return {
        "mensagem": f"{primeiro.nome} foi chamado para atendimento.",
        "cliente_atendido": primeiro,
        "fila_atualizada": clientes_aguardando(),
    }


@app.delete(
    "/fila/{posicao}",
    status_code=status.HTTP_200_OK,
    tags=["Fila"],
)
def remover_cliente(
    posicao: int = Path(..., ge=1, description="Posição que será removida"),
) -> dict:
    """Remove uma pessoa da fila e reorganiza as posições restantes."""

    cliente = localizar_por_posicao(posicao)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe cliente aguardando na posição {posicao}.",
        )

    fila_clientes.remove(cliente)
    reorganizar_apos_remocao(posicao)

    return {
        "mensagem": f"{cliente.nome} foi removido da fila.",
        "fila_atualizada": clientes_aguardando(),
    }

