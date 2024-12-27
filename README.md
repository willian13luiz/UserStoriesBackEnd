# Gerador de Histórias de Usuário

Esta aplicação web em Python utiliza a API da OpenAI para gerar histórias de usuário e seus critérios de aceitação com base na funcionalidade e sistema fornecidos.

## Tecnologias Utilizadas

- Python
- Flask
- OpenAI API

## Configuração

1. **Clone o repositório:**
    bash
    git clone https://seu-repositorio.git
    cd seu-repositorio
    

2. **Crie um ambiente virtual:**
    bash
    python3 -m venv venv
    source venv/bin/activate
    

3. **Instale as dependências:**
    bash
    pip install -r requirements.txt
    

4. **Configure a chave da API da OpenAI:**
    - Renomeie o arquivo `.env.example` para `.env`:
        bash
        mv .env.example .env
        
    - Adicione sua chave da API da OpenAI no arquivo `.env`:
        
        OPENAI_API_KEY=your_openai_api_key_here
        

5. **Execute a aplicação:**
    bash
    python app.py
    

## Endpoints

### Gerar História de Usuário

- **URL:** `/generate_user_story`
- **Método:** `POST`
- **Corpo da Requisição:**
    json
    {
        "functionality": "Descrição da funcionalidade",
        "system": "Nome do sistema"
    }
    
- **Resposta de Sucesso:**
    json
    {
        "user_story": "História de usuário gerada..."
    }
    
- **Resposta de Erro:**
    json
    {
        "error": "Mensagem de erro."
    }
    

## Exemplo de Uso

bash
```
curl -X POST http://localhost:5000/generate_user_story \
     -H "Content-Type: application/json" \
     -d '{
           "functionality": "Autenticação de usuários",
           "system": "Sistema de Gestão de Projetos"
         }'
```