import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from robots import read_robots_txt

# Configurar las opciones de Chrome para ejecutar en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Inicializar el navegador Chrome en modo headless
driver = webdriver.Chrome(options=chrome_options)


class Node:
    # Atributo de clase para memoria dinámica y evitar bucles infinitos
    _visited = []
    _disallowed_urls = None
    _limit = 50
    _counter = 0
    _keywords = []
    search = []

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
        cls._disallowed_urls = read_robots_txt(website)

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

    """
    Función para mostrar el subárbol generado a partir de un nodo en específico de manera recursiva
    
    Recibe: nada
    Devuelve: nada
    """

    @classmethod
    def print_tree(cls, tree, level=0):

        # Para mostrar por niveles
        print(f'|{"---" * level}: {tree.page}')

        if len(tree.children) == 0:
            return

        for child in tree.children:
            cls.print_tree(child, level + 1)

    """
      Obteniendo el dominio de una URI dada.
      Debo de tener en cuenta que un nominio no es un .php, .html, .js, etc.

      Recibe: string -> URI
      Devuelve:
          string -> El dominio de la URI
          None -> Cuando no se encuentra el dominio
      """

    @staticmethod
    def _get_domain(uri):
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
            #         print("uri completa: ", webpage, uri)
            #         print(webpage_match.group(1), domain)

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

        for header in driver.find_elements(By.TAG_NAME, 'h1'):
            if header.accessible_name != '':
                for word in cls._keywords:
                    if word in header.accessible_name.lower():
                        cls.search.append({
                            'title': header.accessible_name,
                            'link': website,
                            'tag': 'h1'
                        })

        for header in driver.find_elements(By.TAG_NAME, 'h2'):
            if header.accessible_name != '':
                for word in cls._keywords:
                    if word in header.accessible_name.lower():
                        cls.search.append({
                            'title': header.accessible_name,
                            'link': website,
                            'tag': 'h2'
                        })

        for header in driver.find_elements(By.TAG_NAME, 'h3'):
            if header.accessible_name != '':
                for word in cls._keywords:
                    if word in header.accessible_name.lower():
                        cls.search.append({
                            'title': header.accessible_name,
                            'link': website,
                            'tag': 'h3'
                        })

        for header in driver.find_elements(By.TAG_NAME, 'h4'):
            if header.accessible_name != '':
                for word in cls._keywords:
                    if word in header.accessible_name.lower():
                        cls.search.append({
                            'title': header.accessible_name,
                            'link': website,
                            'tag': 'h4'
                        })
        for header in driver.find_elements(By.CLASS_NAME, 'enlaces_leido'):
            if header.accessible_name != '':
                for word in cls._keywords:
                    if word in header.accessible_name.lower():
                        actual_website = header.get_attribute('href') if header.tag_name == 'a' else website
                        cls.search.append(
                            {
                                'title': header.accessible_name,
                                'link': actual_website,
                                'class_name': 'enlaces_leido'
                            }
                        )

        for header in driver.find_elements(By.CLASS_NAME, 'enlaces'):
            if header.accessible_name != '':
                for word in cls._keywords:
                    if word in header.accessible_name.lower():
                        actual_website = header.get_attribute('href') if header.tag_name == 'a' else website
                        cls.search.append(
                            {
                                'title': header.accessible_name,
                                'link': actual_website,
                                'class_name': 'enlaces'
                            }
                        )

    @classmethod
    def _search_links(cls, website, domain) -> list:
        links = []

        for link in driver.find_elements(By.TAG_NAME, 'a'):
            uri = link.get_attribute('href')
            if uri is None or len(uri) == 0 or uri == '':
                continue

            uri = cls._uri_cleaner(uri, domain, website)

            if uri is not None and uri not in links and uri != website:
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
            file_re = r'.*\.(docx|doc|pdf|xls|mp4|mp3|mkv|mpeg|png|jpeg|jpg|ico)$'
            file_match = re.search(file_re, website)

            if file_match:
                return None

            domain = Node._get_domain(website)
            if domain is None:
                raise Exception("No se pudo obtener dominio")

            driver.get(website)

            Node._search_content(website)  # Buscando contenido con las palabras clave
            links = Node._search_links(website, domain)  # Buscando links en la página

            return links
        except StaleElementReferenceException:
            pass
        except Exception as e:
            raise Exception(e)
