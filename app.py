from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY não está configurada no arquivo .env")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# Configuração do CORS
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

def gerar_historia(prompt):
    try:
        response = model.generate_content(prompt)
        # Supondo que a resposta contenha o texto gerado em 'text'
        user_story = response.text
        return user_story, None
    except Exception as e:
        return None, str(e)

@app.route('/generate/funcionalidade', methods=['POST', 'OPTIONS'])
def generate_funcionalidade():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight'}), 200

    data = request.get_json()
    funcionalidade = data.get('funcionalidade')
    sistema = data.get('sistema')
    info = data.get('info')  # Atributo opcional

    if not funcionalidade or not sistema:
        return jsonify({'error': 'Funcionalidade e Sistema são obrigatórios!'}), 400

    # Construção do prompt com o atributo "info" caso fornecido
    prompt = (
        f"A história de usuário deve possuir um título conciso e claro. O formato do título deve ser: \"# História de Usuário: Título\""
        f"A sintaxe das histórias de usuários deve ser:  “Como um <tipo de usuário>, eu"
        f"quero <alguma funcionalidade>, para que <algum benefício>”.Os critérios de aceitação devem ser listados como uma lista enumerada."
        f"Como um Analista de Requisitos Ágil, escreva uma história de usuário "
        f"e seus critérios de aceitação com base no seguinte contexto.\n\n"
        f"Sistema: {sistema}\nFuncionalidade: {funcionalidade}\n\n"
    )

    if info:  # Adiciona a informação extra se ela existir
        prompt += f"Informações adicionais: {info}\n\n"

    user_story, error = gerar_historia(prompt)
    if error:
        return jsonify({'error': 'Erro ao se comunicar com a API do Gemini.', 'details': error}), 500

    return jsonify({'message': user_story, 'success': 'A resposta foi gerada com sucesso!'}), 200

@app.route('/generate/tecnica', methods=['POST', 'OPTIONS'])
def generate_tecnica():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight'}), 200

    data = request.get_json()
    descricao_tecnica = data.get('descricao_tecnica')
    sistema = data.get('sistema')

    if not descricao_tecnica or not sistema:
        return jsonify({'error': 'Descrição Técnica e Sistema são obrigatórios!'}), 400

    prompt = (
        f"Como um engenheiro de software, escreva uma história técnica e seus critérios de aceitação com base na seguinte descrição técnica e sistema.\n\n"
        f"Sistema: {sistema}\nDescrição Técnica: {descricao_tecnica}\n\n"
    )

    user_story, error = gerar_historia(prompt)
    if error:
        return jsonify({'error': 'Erro ao se comunicar com a API do Gemini.', 'details': error}), 500

    return jsonify({'message': user_story, 'success': 'A resposta técnica foi gerada com sucesso!'}), 200

@app.route('/generate/desempenho', methods=['POST', 'OPTIONS'])
def generate_desempenho():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight'}), 200

    data = request.get_json()
    requisito_desempenho = data.get('requisito_desempenho')
    sistema = data.get('sistema')

    if not requisito_desempenho or not sistema:
        return jsonify({'error': 'Requisito de Desempenho e Sistema são obrigatórios!'}), 400

    prompt = (
        f"Como um profissional de Engenharia de Requisitos, escreva uma história de usuário focada em desempenho e seus critérios de aceitação com base no seguinte requisito e sistema.\n\n"
        f"Sistema: {sistema}\nRequisito de Desempenho: {requisito_desempenho}\n\n"
    )

    user_story, error = gerar_historia(prompt)
    if error:
        return jsonify({'error': 'Erro ao se comunicar com a API do Gemini.', 'details': error}), 500

    return jsonify({'message': user_story, 'success': 'A história de desempenho foi gerada com sucesso!'}), 200

@app.route('/generate/custom', methods=['POST', 'OPTIONS'])
def generate_custom():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight'}), 200

    data = request.get_json()
    prompt_custom = data.get('prompt')

    if not prompt_custom:
        return jsonify({'error': 'Prompt personalizado é obrigatório!'}), 400

    user_story, error = gerar_historia(prompt_custom)
    if error:
        return jsonify({'error': 'Erro ao se comunicar com a API do Gemini.', 'details': error}), 500

    return jsonify({'message': user_story, 'success': 'A história personalizada foi gerada com sucesso!'}), 200

# Rota para testar o servidor
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'API de Geração de Histórias de Usuário está funcionando!'}), 200

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
