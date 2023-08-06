from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_site():
    url = request.json.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Exemplo simples: extrair todos os títulos de parágrafos (p tags) da página
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        return jsonify({"paragraphs": paragraphs})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # URL do site que contém o formulário
    target_url = 'https://sistemas.anatel.gov.br/Boleto/Internet/Tela.asp'  # substitua pela URL correta da página
    
    cnpj_cpf = request.json.get('NumCNPJCPF')
    fistel = request.json.get('NumFistel')

    if not cnpj_cpf or not fistel:
        return jsonify({"error": "Both NumCNPJCPF and NumFistel are required"}), 400

    data = {
        'NumCNPJCPF': cnpj_cpf,
        'NumFistel': fistel,
        'acao': 'c',
        'cmd': ''
    }

    try:
        response = requests.post(target_url, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Aqui você pode adicionar lógica para extrair informações da resposta, se necessário
        # Por exemplo: verificar se há alguma mensagem de erro na página resultante
        
        return jsonify({"message": "Form submitted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
