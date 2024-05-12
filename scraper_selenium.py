from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import time

"""
Obteniendo el dominio de una URI dada.
Debo de tener en cuenta que un nominio no es un .php, .html, .js, etc.

Recibe: string -> URI
Devuelve:
    string -> El dominio de la URI
    None -> Cuando no se encuentra el dominio
"""


def get_domain(uri):
    try:
        domain_pattern = r'(?:https?:\/\/)?(?:www[2]?\.)?([^\/]+\.(?!php|html)[a-z]+)'
        domain_match = re.search(domain_pattern, uri)
        if domain_match:
            return domain_match.group(1)
        else:
            return None
    except AttributeError as e:
        return None


def uri_cleaner(uri, domain, webpage):
    # Si es un php o html así puesto como si nada, puro nombre y extensión:
    pattern_only_filename = r'(\/?[a-z|A-Z|0-9|_|-]+(\.php|html))'
    only_filename_match = re.search(pattern_only_filename, uri)

    # Si es una página en la misma ruta base
    pattern_webpage = r'([a-z|A-Z|0-9|_|-]+(\.php|html)?$)'
    pattern_uri_filename = r'([a-z|A-Z|0-9|_|-]+(\/.+)?(\.php|html)?$)'  # (\.php|html)?$
    uri_filename_match = re.search(pattern_uri_filename, uri)
    webpage_match = re.search(pattern_webpage, webpage)

    if "#" in uri or 'javascript' in uri or 'mailto' in uri:
        return None

    if "#" in uri:
        return None

    uri_domain = get_domain(uri)

    if uri[0] == '/':
        uri = domain + uri
    elif uri_domain is None:  # or ".php" in uri_domain or ".html" in uri_domain

        if only_filename_match:
            uri = f'{domain}/{uri}'
        elif uri_filename_match and webpage_match.group(1) not in domain:
            uri = webpage.replace(webpage_match.group(1), uri_filename_match.group(1))
        else:
            return None

    elif uri_domain != domain:
        return None

    # Asignando el protocolo https para obtener un objeto correcto para el módulo requests
    if "http" not in uri and "https" not in uri:
        uri = "https://" + uri

        # Quitando el / del final
    if uri[len(uri) - 1] == '/':
        uri = uri[:-1]

    return uri


def scraper(website):
    # Configurar las opciones de Chrome para ejecutar en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Inicializar el navegador Chrome en modo headless
    driver = webdriver.Chrome(options=chrome_options)

    keywords = ['la']

    # Si website tiene un / al final, se le quita
    website = website[:len(website) - 1] if website[len(website) - 1] == "/" else website
    #     website = "/comandos/bienvenido.php"

    # Para evitar que se descarguen archivos
    file_re = r'.*\.(docx|doc|pdf|xls|mp4|mp3|mkv|mpeg|png|jpeg|jpg|ico)$'
    file_match = re.search(file_re, website)

    if file_match:
        return None

    domain = get_domain(website)

    print("req: ", website)
    if domain is None:
        print("No se obtuvo el dominio. Retornando...")
        return
    #         raise Exception("No se pudo obtener dominio")
    driver.get(website)
    time.sleep(2)

    links = []
    uri = None
    try:
        for link in driver.find_elements(By.TAG_NAME, 'a'):
            uri = link.get_attribute('href')
            if uri is None or uri == '':
                continue

        # uri = uri_cleaner(uri, domain, website)
        #
        # if uri is not None and uri not in links and uri != website:
        #     links.append(uri)

    except:
        pass

    headers = {
        'h1': [],
        'h2': [],
        'h3': [],
        'meta_description': [],
        'keywords': []
    }

    search = set()

    headers_tags = ['h1', 'h2', 'h3', 'h4', 'meta']
    for tag_name in headers_tags:
        headers = driver.find_elements(By.TAG_NAME, tag_name)
        for header in headers:
            text = header.text
            if tag_name == 'meta' and header.get_attribute('property') == 'og:description':
                text = header.get_attribute('content')

            if text:
                if any(word in text.lower() for word in keywords):
                    search.add((text, website, tag_name))

    headers_divs = ['divRubro']
    for div_name in headers_divs:
        headers = driver.find_elements(By.ID, div_name)
        for header in headers:
            text = header.text
            if text:
                if any(word in text.lower() for word in keywords):
                    search.add((text, website, div_name))

    element_classes = ['enlaces_leido', 'enlaces', 'breadcrum']
    for element_class in element_classes:
        elements = driver.find_elements(By.CLASS_NAME, element_class)
        for element in elements:
            if element.text and element.tag_name != 'td':
                actual_website = element.get_attribute('href') if element.tag_name == 'a' else website
                if any(word in element.text.lower() for word in keywords):
                    search.add((element.text, actual_website, element_class))

    # print("\n".join(links))
    print("keywords: ", keywords)
    print("Información encontrada:")
    # print(headers)
    for content in search:
        print("\t", content[0])
        print(content[1])
        print("-------")


if __name__ == '__main__':
    scraper('https://www.dof.gob.mx/nota_detalle.php?codigo=5725572&fecha=06/05/2024#gsc.tab=0')
