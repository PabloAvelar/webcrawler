import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from utils.robots import read_robots_txt

# Configurar las opciones de Chrome para ejecutar en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
#Lo

# Inicializar el navegador Chrome en modo headless
driver = webdriver.Chrome(options=chrome_options)

class Node:
    # Atributo de clase para memoria dinámica y evitar bucles infinitos
    _visited = []
    _disallowed_urls = None
    _limit = 20
    _counter = 0
    _keywords = []
    search = set()

    def __init__(self, parent=None, children=None, page=None):
        if children is None:
            children = []

        self._parent = parent
        self._children = children
        self._page = page

    @property
    def page(self):
        return self._page

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children.append(value)

    @classmethod
    def read_robots(cls, website: str) -> None:
        get_robots = read_robots_txt(website)
        cls._disallowed_urls = get_robots if get_robots is not None else []

    @classmethod
    def set_keywords(cls, keywords: list) -> None:
        cls._keywords = keywords

    def crawl(self, tree):
        file_re = r'.*\.(docx|doc|pdf|xls)$'
        file_match = re.search(file_re, tree.page)

        if file_match:
            return None

        if Node._counter >= Node._limit:
            return

        if ".xlsx" in tree.page or ".pdf" in tree.page:
            return

        Node._counter += 1
        print("crawling: ", tree.page)

        links = self._scraper(tree.page)
        if links is None:
            return
        if len(links) == 0:
            return

        for link in links:
            new_child = Node(parent=tree, children=None, page=link)
            tree.children = new_child
            

        # Haciendo mismo procedimiento para cada hijo de manera recursiva
        for child in tree.children:
            
            self.crawl(child)



    @classmethod
    def print_tree(cls, tree, level=0):
        """
        Función para mostrar el subárbol generado a partir de un nodo en específico de manera recursiva

        :argument tree: subárbol
        :argument level: nivel del subárbol
        :return None
        """

        # Para mostrar por niveles
        print(f'|{"---" * level}: {tree.page}')
        

        if len(tree.children) == 0:
            return

        for child in tree.children:
            
            cls.print_tree(child, level + 1)
            


    @staticmethod
    def _get_domain(uri):
        """
          Obteniendo el dominio de una URI dada.
          Debo de tener en cuenta que un nominio no es un .php, .html, .js, etc.

          :argument uri: string
          :return string: El dominio de la URI
          :return None: Cuando no se encuentra el dominio
          """
        try:
            domain_pattern = r'(?:https?:\/\/)?(?:www\.)?([^\/]+\.(?!php|html)[a-z]+)'
            domain_match = re.search(domain_pattern, uri)
            
            if domain_match:
                
                return domain_match.group(1)
            else:
                
                return None
        except AttributeError as e:
            return None

    @staticmethod
    def _uri_cleaner(uri, domain, webpage):
        # Si es un php o html así puesto como si nada, puro nombre y extensión:
        pattern_only_filename = r'([a-z|A-Z|0-9|_|-]+(\.php|html))'
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

        uri_domain = Node._get_domain(uri)

        if uri[0] == '/':
            uri = domain + uri
        elif uri_domain is None:  # or ".php" in uri_domain or ".html" in uri_domain

            if only_filename_match:
                uri = f'{domain}/{uri}'
            elif uri_filename_match and webpage_match.group(1) not in domain:
                uri = webpage.replace(webpage_match.group(1), uri_filename_match.group(1))
            else:
                return None

        # Si el link es de una página externa
        elif uri_domain != domain:
            return None

        # Asignando el protocolo https para obtener un objeto correcto para el módulo requests
        if "http" not in uri and "https" not in uri:
            uri = "https://" + uri

        # Quitando el / del final
        if uri[len(uri) - 1] == '/':
            uri = uri[:-1]

        return uri

    @classmethod
    def _search_content(cls, website) -> None:
        headers_tags = ['h1', 'h2', 'h3', 'h4', 'h5']
        for tag_name in headers_tags:
            headers = driver.find_elements(By.TAG_NAME, tag_name)
            for header in headers:
                if header.text:
                    if any(word in header.text.lower() for word in cls._keywords):
                        cls.search.add((header.text, website, tag_name))

        id_divs = ['divRubro']
        for div in id_divs:
            headers = driver.find_elements(By.ID, div)
            for element in headers:
                if element.text:
                    if any(word in element.text.lower() for word in cls._keywords):
                        cls.search.add((element.text, website, div))

        element_classes = ['enlaces_leido', 'enlaces', 'txt_blanco']
        for element_class in element_classes:
            elements = driver.find_elements(By.CLASS_NAME, element_class)
            for element in elements:
                if element.text and element.tag_name != 'td':
                    actual_website = element.get_attribute('href') if element.tag_name == 'a' else website
                    if any(word in element.text.lower() for word in cls._keywords):
                        cls.search.add((element.text, actual_website, element_class))

    @classmethod
    def _search_links(cls, website, domain) -> list:
        links = []

        for link in driver.find_elements(By.TAG_NAME, 'a'):
            uri = link.get_attribute('href')
            if uri is None or len(uri) == 0 or uri == '':
                continue

            uri = cls._uri_cleaner(uri, domain, website)

            if uri is not None and uri not in links and uri != website:
                uri = uri.replace('http://', 'https://')
                if "https://www." not in uri and domain != 'egaceta.scjn.gob.mx':
                    uri = uri.replace("https://", "https://www.")
                if uri not in cls._visited and uri not in cls._disallowed_urls:
                    links.append(uri)
                    cls._visited.append(uri)

        return links

    def _scraper(self, website):
        try:
            # Si website tiene un / al final, se le quita
            website = website[:len(website) - 1] if website[len(website) - 1] == "/" else website
            Node._visited.append(website)

            # Para evitar que se descarguen archivos
            file_re = r'.*\.(docx|doc|pdf|xlsx|mp4|mp3|mkv|mpeg|png|jpeg|jpg|ico)$'
            file_match = re.search(file_re, website)

            if file_match:
                return None

            domain = Node._get_domain(website)
            if domain is None:
                raise Exception("No se pudo obtener dominio")

            driver.get(website)
            if domain == 'egaceta.scjn.gob.mx':
                time.sleep(1)

            Node._search_content(website)  # Buscando contenido con las palabras clave
            links = Node._search_links(website, domain)  # Buscando links en la página

            return links
        except StaleElementReferenceException:
            pass
        except Exception as e:
            raise Exception(e)
        

