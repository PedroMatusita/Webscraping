from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Encontrar todas as marcas
url = 'https://www.drogariasminasmais.com.br/medicamentos'
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

marcas = soup.find_all("label", class_="vtex-checkbox__label w-100 c-on-base pointer")
marcas_corr = []
for marca in marcas:
    marcas_corr.append(str(marca).split('>')[1].split('<')[0])
for i in range(len(marcas_corr)):
    marcas_corr[i] = marcas_corr[i].lower().replace(" ", '-')
marcas_corr = marcas_corr[19:]

# Encontrar todas urls dos medicamentos
URLS=[]

for marca in marcas_corr:
    url = 'https://www.drogariasminasmais.com.br/medicamentos/'+marca+'?initialMap=c&initialQuery=medicamentos&map=category-1,brand&page=1'
    print(url)
    driver = webdriver.Chrome()
    driver.get(url)
    parada = int(driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/div/div[2]/div/div/section/div[2]/div/div[3]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[1]/div/span").text.strip().split(' ')[0])
    print('número de medicamentos:', parada)
    for i in range(1, 30):
        url = "https://www.drogariasminasmais.com.br/medicamentos/"+marca+"?initialMap=c&initialQuery=medicamentos&map=category-1,brand&page="+str(i)
      
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        medicamentos = soup.find_all("div", class_="vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4")
    
        for medicamento in medicamentos:
            URLmed = "https://www.drogariasminasmais.com.br" + medicamento.find("a", class_='vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--product__summary vtex-product-summary-2-x-clearLink--product__summary--shelf h-100 flex flex-column').get('href')
          
            URLS.append(URLmed)
        print(i)
        print(len(URLS))
        if (i) > parada/15:
            break



# Pegar as informações necessárias de cada medicamento em cada url

driver = webdriver.Chrome()
for url in URLS:
    
    driver.get(url)
    
    nome = driver.find_element(By.CLASS_NAME,"vtex-store-components-3-x-productBrand ").text.strip()
    print (nome)
    preco = driver.find_element(By.CSS_SELECTOR, '.vtex-product-price-1-x-sellingPrice--product__price--hasListPrice').text.strip()
    print (preco)
    preco_antigo = driver.find_element(By.CSS_SELECTOR, '.vtex-product-price-1-x-listPrice--product__price').text.strip()
    print(preco_antigo)


driver.quit()
