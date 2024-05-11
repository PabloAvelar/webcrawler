import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import html
import urllib3


def get_sumario(url):
    urllib3.disable_warnings()
    url_sumario = url.rstrip("/") + '/sumario.xml'
    response = requests.get(url_sumario, verify=False)

    try:
        if response.status_code == 200:
            # Parseando a XML
            tree = ET.ElementTree(ET.fromstring(response.content))
            root = tree.getroot()
            return root
    except ParseError:
        print('No es xml')

    return None


def results(search):
    for result in search:
        print(f'\t{result[0]} ({result[1]})')
        print(result[2])
        print(result[3])
        print("----------------------------")

def scrape_sumario(sumario, keywords):
    items = sumario.findall('.//item')
    search = set()

    for item in items:
        title_tag = item.find('.//title')
        description_tag = item.find('.//description')
        link_tag = item.find('.//link')
        valueDate_tag = item.find('.//valueDate')

        title = html.unescape(title_tag.text)
        description = html.unescape(description_tag.text)
        link = html.unescape(link_tag.text)
        valueDate = html.unescape(valueDate_tag.text)

        if len(keywords) > 0:
            for kw in keywords:
                if kw.lower() in title.lower() or kw.lower() in description.lower():
                    search.add((title, valueDate, description, link))

            # Mostrando resultados

        else:
            search.add((title, valueDate, description, link))

    results(search)

# sumario = get_sumario('https://www.dof.gob.mx/')
# scrape_sumario(sumario, ['jalisco'])
