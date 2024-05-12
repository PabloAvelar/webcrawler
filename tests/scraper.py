import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
        domain_pattern = r'(?:https?:\/\/)?(?:www\.)?([^\/]+\.(?!php|html)[a-z]+)'
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

    if "#" in uri or 'javascript' in uri:
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

    elif uri_domain != domain:
        return None

    # Asignando el protocolo https para obtener un objeto correcto para el módulo requests
    if "http" not in uri and "https" not in uri:
        uri = "https://" + uri

        # Quitando el / del final
    if uri[len(uri) - 1] == '/':
        uri = uri[:-1]

    return uri


forms_action = []


def scraper():
    headers = {
        'User-Agent': UserAgent().chrome
    }

    website = "https://dof.gob.mx/"

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
    r = None
    try:
        r = requests.get(website, headers=headers)
    except requests.exceptions.SSLError:
        # print("No se pudo verificar SSL")
        r = requests.get(website, headers=headers, verify=False)
    except:
        print("Error en la petición GET")

    soup = BeautifulSoup(r.content, 'lxml')
    links = []

    for action in soup.find_all('form', method='get'):
        #         print(action)
        forms_action.append(action)

    for link in soup.find_all('a', href=True):
        uri = link.get('href')
        if len(uri) == 0:
            continue

        uri = uri_cleaner(uri, domain, website)

        if uri is not None and uri not in links and uri != website:
            links.append(uri)

    print("\n".join(links))

    print("Descargando la página...")
    with open("pagina.html", 'w+', encoding='utf-8') as file:
        file.write(soup.prettify())


if __name__ == '__main__':
    scraper()
