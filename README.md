# API da Fila de Atendimento da Anna

Projeto final da disciplina **Desenvolvimento de APIs e Microserviços**, desenvolvido por **Anna Julia Torres Martins de Deus** com Python e FastAPI.

A API simula o funcionamento de um totem de atendimento presencial. Ela permite adicionar clientes, consultar a fila, chamar a próxima pessoa e remover alguém da fila. Também foi implementado o requisito bônus de atendimento prioritário.

## Regras utilizadas

- O nome é obrigatório e aceita no máximo 20 caracteres.
- O tipo de atendimento aceita somente `N` para normal ou `P` para prioritário.
- Clientes prioritários ficam antes dos clientes normais.
- Uma nova prioridade entra depois das outras prioridades que já aguardam.
- O cliente chamado sai da posição 1, passa para a posição 0 e recebe `atendido = true`.
- Os dados ficam armazenados em memória e são reiniciados quando o servidor é fechado.

## Endpoints

| Método | Rota | Função |
|---|---|---|
| GET | `/fila` | Lista os clientes não atendidos |
| GET | `/fila/{posicao}` | Consulta uma posição da fila |
| POST | `/fila` | Adiciona um cliente normal ou prioritário |
| PUT | `/fila` | Chama o primeiro cliente e atualiza as posições |
| DELETE | `/fila/{posicao}` | Remove um cliente e reorganiza a fila |

## Como executar

No terminal do VS Code:

```powershell
py -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

```powershell
py -m pip install -r requirements.txt
```

```powershell
py -m uvicorn main:app --reload
```

Abra a documentação interativa:

```text
http://127.0.0.1:8000/docs
```

## Exemplo para o POST

Cliente normal:

```json
{
  "nome": "Mariana",
  "tipo": "N"
}
```

Cliente prioritário:

```json
{
  "nome": "Carlos",
  "tipo": "P"
}
```

## Testes automáticos

Execute:

```powershell
py -m pytest -v
```

Os testes verificam a fila vazia, cadastro normal, prioridade, consulta, atendimento, remoção, validações e retornos 404.

## Tecnologias

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX

