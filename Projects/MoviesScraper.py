import requests
import json
from bs4 import BeautifulSoup 
from APIs.oraModel import Model

# Chamando Função para enviar Mensagem a API
ora = Model()

# Função para Pesquisar o site no Site Alvo

def SearchMovie(page, query):
    if page == None:
        page = 1

    # Site alvo

    returnBaseObject = {
            "Movies": {}
        }
    site = f"https://filmesviatorrents.net/page/{page}/?s={query}"
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
    }

    # Realizando WebScraping a partir dos dados fornecidos

    r = requests.get(site, headers=headers)
    if r.status_code != 200:
        return print(f"ERROR! STATUS_CODE: [{r.status_code}]")
    
    html = r.content
    bs = BeautifulSoup(html, "html.parser")
    results = bs.find_all("h2", {"class": "entry-title"})
    count = 0

    for x in results:
        count += 1

        # Preparando o return dos dados

        titles = x.find("a").get_text()
        links = x.find("a")['href']
        moviesJson = {
            count: {
                "title": titles,
                "links": links,
                "id": count
            }
        }
        returnBaseObject["Movies"].update(moviesJson)
    return returnBaseObject


# Função para Extrair o Magnet URL do site Alvo
# Modificado para extrair outras informações

def ScraperMagnetURL(url_base):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
    }
    infoObject = {
        "magnet": "",
        "total_size": ""
    }
    r = requests.get(url_base, headers=headers)
    if r.status_code != 200:
        return print(f"ERROR! STATUS_CODE: [{r.status_code}]")
    html = r.content
    bs = BeautifulSoup(html, "html.parser")
    allResults = bs.find_all('div', {'class': 'entry-content cf'}) 

    for p in allResults:
        file_size = p.get_text()[198:204].strip()
        infoObject["total_size"] = file_size
        for a in p.find_all('p'):
            magnetURL = a.find('a')
            if hasattr(magnetURL, 'href'):
                if magnetURL['href'].startswith('magnet'):
                    infoObject["magnet"] = magnetURL['href'] 

    return infoObject

# Pegando Input do Usuario para realizar a Pesquisa

inputMovie = input("Digite o nome do filme a ser Pesquisado: ")
movies = SearchMovie(1, inputMovie)

# Formatando response para a IA entender

moviesObject = []

for key, values in movies['Movies'].items():
    stringforIA = f"{values['id']}. {values['title']}\n"
    moviesObject.append(stringforIA)
moviesOBJFormatted = ''.join(moviesObject)

# Realizando o envio dos filmes para ser classificado e filtrado
message = f'{moviesOBJFormatted}\n Based on the items above, answer which item correlates more with f"{inputMovie}". Do not include any other explanatory text in your response only number.\nIf none of them match, just reply with the number 0\n Follow this format to response:\n <Number>'
classificationMovie = ora.sendMessage(message)

# Puxando o Filme filtrado

filterMovie = movies["Movies"][int(classificationMovie)]

# Puxando Informações do Filme 
# Filtrando Titulo
titleFilterMessage = f"{filterMovie['title']}\n Based on the items above, Extract the title of the movie, related to '{inputMovie}', Do not include any other explanatory text in your response.\n Follow this format to response:\n <Title of Movie>"
titleFilter = ora.sendMessage(titleFilterMessage)

# Pegando Tamanho Real do Torrent e o Link Magnet
movieInfo = ScraperMagnetURL(filterMovie['links'])

# Messagem Final
baseMessage = f""" 

**Nome do Filme: {titleFilter}**
**Ano de Lançamento: 
**Gênero: || ||**
**Dublado: ||Sim||**
**Legendado: ||Não||**

**Sinopse:**

**Duração:** || ||**
**Qualidade: || ||**
**Formato: ||MKV||**

:inbox_tray: Link para Download :inbox_tray: 

||{movieInfo['magnet']}||
**Tamanho Estimado:** **||{movieInfo['total_size']} GB||**

@Filmes

"""

print(baseMessage)





