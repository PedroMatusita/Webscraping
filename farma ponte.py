import requests
from bs4 import BeautifulSoup
import pandas as pd
URLS=[]

for i in range(228):
    # URL da página de medicamentos
    url = "https://www.farmaponte.com.br/medicamentos/?p="+str(i)

    # Requisição à página
    response = requests.get(url)
    # Criar objeto BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Encontrar os containers dos medicamentos
    medicamentos = soup.find_all("div", class_="item-product")
    # Extrair dados para cada medicamento
    for medicamento in medicamentos:
        nome = medicamento.find("h2", class_="title").text.strip()
        try:
            preco = medicamento.find("p", class_="pix-price").text.strip()
        except: 
            preco='sem'
        URL = "https://www.farmaponte.com.br" + medicamento.find("a", class_='item-image').get('href')
        # Imprimir dados
        URLS.append(URL)
    print(i)
print(len(URLS))
print(URLS[0])
NOME = []
PRECO=[]
EAN=[]

# URL da página de medicamentos
for url in URLS:

    # Requisição à página
    response = requests.get(url)
    # Criar objeto BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Encontrar os containers dos medicamentos
    medicamentos = soup.find_all("div", class_="content")

    # Extrair dados para cada medicamento
    for medicamento in medicamentos:
        try:
            nome = medicamento.find("h1", class_="name").text.strip()
        except:
            nome = 'sem'
        try:
            preco = medicamento.find("div", class_="pix-price").text.strip()
        except:
            preco = 'sem'
        try:
            ean = medicamento.find(itemprop="gtin13").get('content')
        except:
            ean = 'sem'
        NOME.append(nome)
        PRECO.append(preco)
        EAN.append(ean)

df = pd.DataFrame()
df['Nome'] = NOME
print('1/3')
df['preco'] = PRECO
print('2/3')
df['ean'] = EAN
print('3/3')

print(df)