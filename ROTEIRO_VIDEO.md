# Roteiro do vídeo final

O vídeo deve ter no máximo 10 minutos. Fale devagar e mostre a tela enquanto explica.

## 0:00 a 0:40 - Apresentação

Olá, meu nome é Anna Julia Torres Martins de Deus. Neste vídeo vou apresentar minha API de fila de atendimento presencial, desenvolvida em Python com o framework FastAPI. O projeto permite cadastrar clientes, consultar a fila, chamar a próxima pessoa e remover registros. Também implementei o atendimento prioritário.

## 0:40 a 2:00 - Estrutura do código

Mostrar o arquivo `main.py`.

Primeiro, importei o FastAPI, o Pydantic e os recursos usados para trabalhar com data, validações e erros. Depois criei a aplicação e defini dois modelos. O modelo NovoCliente recebe o nome e o tipo de atendimento. O modelo ClienteFila representa o registro completo, com posição, nome, data de chegada, tipo e a informação se o cliente já foi atendido.

O campo nome é obrigatório e aceita no máximo 20 caracteres. O tipo aceita somente N, para atendimento normal, ou P, para atendimento prioritário.

## 2:00 a 3:00 - Funções auxiliares

Mostrar `clientes_aguardando`, `localizar_por_posicao` e `reorganizar_apos_remocao`.

Criei funções auxiliares para organizar o código. Uma lista somente os clientes que ainda aguardam, outra procura uma pessoa pela posição e a última corrige as posições depois de uma exclusão.

## 3:00 a 4:00 - GET da fila

Abrir `http://127.0.0.1:8000/docs`.

O endpoint GET barra fila lista as pessoas que ainda não foram atendidas. Como a fila está vazia, ele retorna uma lista JSON vazia e o status 200.

Agora vou cadastrar clientes para demonstrar os outros endpoints.

## 4:00 a 5:30 - POST e prioridade

Cadastrar Mariana com tipo N e Rafael com tipo N. Depois cadastrar Dona Lúcia com tipo P.

O endpoint POST barra fila recebe o nome e o tipo. A API cria a data de chegada, define atendido como falso e calcula a posição. Dona Lúcia recebeu a posição 1 porque o atendimento é prioritário, enquanto os clientes normais foram deslocados.

Mostrar também uma tentativa com tipo X para demonstrar a validação.

## 5:30 a 6:30 - GET por posição e erro 404

No GET barra fila barra posição, vou pesquisar a posição 1. A API encontrou Dona Lúcia e retornou os dados dela.

Agora vou pesquisar a posição 99. Como ela não existe, a API retorna o status 404 e uma mensagem explicativa.

## 6:30 a 7:30 - PUT para chamar o próximo

O endpoint PUT barra fila chama a pessoa da posição 1. Ela passa para a posição 0, o campo atendido passa para verdadeiro e as outras pessoas avançam uma posição.

## 7:30 a 8:20 - DELETE

O endpoint DELETE remove a pessoa da posição informada. Depois da exclusão, a API reorganiza as posições para não deixar espaços na fila. Uma posição inexistente também retorna o status 404.

## 8:20 a 9:20 - GitHub e encerramento

Mostrar rapidamente o repositório público no GitHub.

Todo o código-fonte está publicado neste repositório público. Também criei testes automáticos para conferir a fila vazia, os cadastros, a prioridade, as consultas, o atendimento, a exclusão e as validações.

Com isso, apresentei o funcionamento da API de fila de atendimento, seus endpoints e o sistema de prioridade. Obrigada.

