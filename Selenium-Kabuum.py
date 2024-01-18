# -> Pips
# pip install pandas
# pip install selenium

import pandas as pd
import math
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as condicao_esperada

# Inicializando as configurações do Chrome
chrome_options = Options()

arguments = ['--lang=pt-BR', '--disable-notifications', "--headless"]
for argument in arguments:
    chrome_options.add_argument(argument)
chrome = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(
    chrome,
    10,
    poll_frequency=1,
    ignored_exceptions=[
        NoSuchElementException,
        ElementNotVisibleException,
        ElementNotInteractableException
    ]
)

url = "https://www.kabum.com.br/tv/smart-tv"
chrome.get(url)

qtd_produtos = wait.until(condicao_esperada.element_to_be_clickable((By.ID, "listingCount")))
qtd_produtos = qtd_produtos.text

numeros = re.findall(r'\d+', qtd_produtos)

qtd = int(numeros[0])
ultima_pag = math.ceil(qtd/20)

dic_produtos = {"NOME TV":[], "PRECO":[], "LINK TV": []}
for i in range(1, ultima_pag+1):
    url_pag = f"https://www.kabum.com.br/tv/smart-tv?page_number={i}"
    chrome.get(url_pag)

    produtos = wait.until(condicao_esperada.visibility_of_all_elements_located((By.CLASS_NAME, "productCard")))
    chrome.implicitly_wait(10)

    for produto in produtos:
        chrome.execute_script("window.scrollTo(0, 200);")

        prdt_nome = chrome.find_element(By.CLASS_NAME, "nameCard").text
        prdt_preco = chrome.find_element(By.CLASS_NAME, "priceCard").text
        prdt_link = chrome.find_element(By.CLASS_NAME, "productLink").get_attribute("href")

        dic_produtos["NOME TV"].append(prdt_nome)
        dic_produtos["PRECO"].append(prdt_preco)
        dic_produtos["LINK TV"].append(prdt_link)

df = pd.DataFrame(dic_produtos)
df.to_csv("SmartTV.csv", encoding="utf-8", sep=";")

print("Fim! Arquivo criado com sucesso.")
