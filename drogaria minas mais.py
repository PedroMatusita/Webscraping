from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.drogariasminasmais.com.br/medicamentos'

# Requisição à página
response = requests.get(url)
# Criar objeto BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
# Encontrar os containers dos medicamentos
marcas = soup.find_all("label", class_="vtex-checkbox__label w-100 c-on-base pointer")
marcas_corr = []
for marca in marcas:
    marcas_corr.append(str(marca).split('>')[1].split('<')[0])
for i in range(len(marcas_corr)):
    marcas_corr[i] = marcas_corr[i].lower().replace(" ", '-')


URLS=[]

for marca in marcas_corr:
# Loop para navegar por várias páginas
    for i in range(1, 20):
        url = "https://www.drogariasminasmais.com.br/medicamentos/"+marca+"?initialMap=c&initialQuery=medicamentos&map=category-1,brand&page="+str(i)
        print(url)
        # Requisição à página
        response = requests.get(url)
        # Criar objeto BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Encontrar os containers dos medicamentos
        medicamentos = soup.find_all("div", class_="vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4")
        # Extrair dados para cada medicamento
    
        for medicamento in medicamentos:
            URL = "https://www.drogariasminasmais.com.br" + medicamento.find("a", class_='vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--product__summary vtex-product-summary-2-x-clearLink--product__summary--shelf h-100 flex flex-column').get('href')
            # Imprimir dados
            URLS.append(URL)
        print(i)
    print(len(URLS))
    print(URLS)



from selenium import webdriver
from selenium.webdriver.common.by import By

# Configurar o WebDriver
driver = webdriver.Chrome()
for url in URLS:
    # Acessar a página de medicamentos
    driver.get(url)
    # Extrair dados para cada medicamento
    nome = driver.find_element(By.CLASS_NAME,"vtex-store-components-3-x-productBrand ").text.strip()
    print (nome)
    preco = driver.find_element(By.CSS_SELECTOR, '.vtex-product-price-1-x-sellingPrice--product__price--hasListPrice').text.strip()
    print (preco)
    preco_antigo = driver.find_element(By.CSS_SELECTOR, '.vtex-product-price-1-x-listPrice--product__price').text.strip()
    print(preco_antigo)

# Fechar o navegador
driver.quit()
