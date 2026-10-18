# Manual passo a passo

## 1. Abrir o projeto

1. Extraia o arquivo ZIP.
2. Abra o Visual Studio Code.
3. Clique em **Arquivo > Abrir Pasta**.
4. Escolha a pasta `api_fila_atendimento_anna`.
5. Clique em **Terminal > Novo Terminal**.

## 2. Criar e ativar o ambiente virtual

Execute:

```powershell
py -m venv .venv
```

Depois:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando funcionar, aparecerá `(.venv)` no início da linha do terminal.

## 3. Instalar as dependências

```powershell
py -m pip install -r requirements.txt
```

## 4. Executar a API

```powershell
py -m uvicorn main:app --reload
```

Não feche o terminal enquanto estiver testando. Abra no navegador:

```text
http://127.0.0.1:8000/docs
```

## 5. Testar pelo Swagger

Em cada endpoint, clique em **Try it out**, preencha os dados quando necessário e clique em **Execute**.

### Teste 1 - Fila vazia

Execute `GET /fila`. O resultado deve ser:

```json
[]
```

com o status `200`.

### Teste 2 - Cadastrar clientes normais

Execute `POST /fila` com:

```json
{
  "nome": "Mariana",
  "tipo": "N"
}
```

Depois cadastre:

```json
{
  "nome": "Rafael",
  "tipo": "N"
}
```

### Teste 3 - Cadastrar uma prioridade

Execute novamente `POST /fila`:

```json
{
  "nome": "Dona Lúcia",
  "tipo": "P"
}
```

Ao executar `GET /fila`, Dona Lúcia deverá aparecer na posição 1, antes dos atendimentos normais.

### Teste 4 - Consultar uma posição

Em `GET /fila/{posicao}`, informe `1`. Depois informe `99` para mostrar o retorno `404`.

### Teste 5 - Chamar o próximo cliente

Execute `PUT /fila`. A pessoa da posição 1 ficará com posição 0 e `atendido = true`. As outras pessoas avançarão uma posição.

### Teste 6 - Remover uma pessoa

Em `DELETE /fila/{posicao}`, informe uma posição existente. Depois use uma posição inexistente para demonstrar o status `404`.

### Teste 7 - Demonstrar as validações

Em `POST /fila`, tente cadastrar o tipo `X` ou um nome com mais de 20 caracteres. O FastAPI recusará os dados e retornará o status `422`.

## 6. Executar os testes automáticos

Pare o servidor com `Ctrl + C` e execute:

```powershell
py -m pytest -v
```

## 7. Configurar o Git somente para o projeto da Anna

```powershell
git config user.name "Anna Julia Torres Martins de Deus"
```

```powershell
git config user.email "anninhamt2605@gmail.com"
```

Confira:

```powershell
git config --get user.name
git config --get user.email
```

## 8. Publicar no GitHub

Crie na conta `anninhamt2605-pixel` um repositório público chamado:

```text
api-fila-atendimento-anna
```

No terminal do projeto, execute um comando por vez:

```powershell
git init
git branch -M main
git add .
git commit -m "Desenvolve API da fila de atendimento"
git remote add origin https://github.com/anninhamt2605-pixel/api-fila-atendimento-anna.git
git push -u origin main
```

Se o navegador pedir autorização, entre com a conta da Anna.

## 9. Links para a entrega

Repositório esperado:

```text
https://github.com/anninhamt2605-pixel/api-fila-atendimento-anna
```

Depois de gravar o vídeo, coloque no AVA o link do GitHub e o link do vídeo configurado para qualquer pessoa com o link.

