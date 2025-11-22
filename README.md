# projeto_ibmec_01
Projeto para Avaliação da Disciplina de Engenharia de Software, Prof. Luis Fernando Lufe Mello Barreto - MBA/IBMEC
Estudantes: Henrique Pimentel, Felipe Gouveia, Rodrigo Barros, Suellyn Schopping

Trata-se de uma aplicação tipo FastAPI para listar produtos por um detemrinado ID e validar cupons de desconto.

Os produtos estão definidos em uma variável em src/api/main.py. Em um caso real seria necessário a conexão com banco de dados.

Foi inserida uma classe CupomDesconto para gerenciar e validar os cupons informados via api.

Para instalar o repositório:

1)  Clone o repositório

    git clone https://github.com/hen-ri-que/projeto_ibmec_01.git

2)  Instala o ambiente virtual

    python -m venv venv 

3) Ativa o ambiente virtual (windows)

   ./venv/Script/activate

4) Atualiza o pip
   
    python -m pip install pip --upgrade

6)  Instala as dependências de requirements.txt
   
    pip install -r requirements.txt

8) Rode a aplicação com uvicorn ou execute
   
    uvicorn src.api.main:app --reload
    

9) Acessar a API no navegador

    utilize o endereço http://127.0.0.1:8000/

10) Health check - exibe o status e a versão

    acesse: http://127.0.0.1:8000/health

11) Para acessar o Swagger UI (documentação automática da API)

   acesse: http://127.0.0.1:8000/docs

   Isso permitirá:
   - a visualização de todas as toras (GET/POST)
   - ver os modelos de entrada/saúda (schemas);
   - testar a API diretamente pelo navegador.

12) Testando os Endpoints:

    - HealthCheck: clique em GET /health
        Try it out
        Execute

    - Produtos: clique em GET /produtos
        Try it out
        Execute

    - Produto específico: clique em GET /produtos/{oroduto_id}
        Try it out
        informe um id válido (p. ex.: 1)
        Execute

    - Aplicar cupom de desconto: clique em POST /produtos/{produto_id}/calcular_desconto
        Try it out
        informe um ID válido (p. ex.: 1)
        no corpo da requisição (Request Body), informe o JSON seguindo o schema cupomInput
        Execute
        A resposta mostra o valor com o desconto aplicado

Observações: 
1. Esse projeto é apenas um exemplo acadêmico; em um cenário real, a fonte de dados de produtos e cupons seria um banco de dados ou outro serviço externo.

2. Para o endpoint de cálculo de desconto, usamos pytest.approx na comparação do campo desconto_percentual, pois o cálculo em ponto flutuante retornava 9.999999999999998 em vez de 10.0. Essa é uma imprecisão numérica comum em operações com float em Python, e o uso de approx garante que o teste verifique o valor esperado dentro de uma tolerância adequada.

3. Para interromper a API, pressione CTRL + C no terminal onde o uvicorn está sendo executado.