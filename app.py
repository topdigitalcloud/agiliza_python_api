from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/interact', methods=['POST'])
def interact_with_site():
    url = request.json.get('url')
    cnpj_cpf = request.json.get('cnpj_cpf')
    fistel = request.json.get('fistel')
    
    if not url or not cnpj_cpf or not fistel:
        return jsonify({"error": "URL, CNPJ/CPF, and Fistel are required"}), 400

    options = webdriver.ChromeOptions()
    # Se eventualmente você for adaptar para um servidor sem interface gráfica, descomente a linha abaixo.
    # options.add_argument("--headless")
    
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")


    try:
        driver.get(url)
        
        # Preencher CNPJ/CPF e Fistel
        driver.find_element(By.ID, "NumCNPJCPF").send_keys(cnpj_cpf)
        driver.find_element(By.ID, "NumFistel").send_keys(fistel)

        # Clicar no botão de confirmação
        driver.find_element(By.ID, "botaoFlatConfirmar").click()

        # Aguardar e clicar no botão "OK" do modal
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='OK']]"))).click()
        
        # A partir daqui, você pode adicionar outras ações ou extrair informações da página, conforme necessário.

        return jsonify({"message": "Successfully navigated and interacted with the page."})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Garantir que o navegador seja fechado após a conclusão
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
