import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Node:
    # Atributo de clase para memoria dinámica y evitar bucles infinitos
    visited = []

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

    def crawl(self, tree):

        print("crawling: ", tree.page)
        links = self._scraper(tree.page)

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
        # Si es una página en la misma ruta base
        pattern_webpage = r'([a-z|A-Z|0-9]+(\.php|html)?$)'
        pattern_uri_filename = r'([a-z|A-Z|0-9]+(\/.+)?(\.php|html)?$)'  # (\.php|html)?$
        uri_filename_match = re.search(pattern_uri_filename, uri)
        webpage_match = re.search(pattern_webpage, webpage)

        if "#" in uri:
            return None
        uri_domain = Node._get_domain(uri)

        if uri_domain is None:  # or ".php" in uri_domain or ".html" in uri_domain
            uri = f'{webpage}/{uri}' if uri[0] != '/' else domain + uri
            # Si el link es de una página externa
        elif uri_domain != domain:
            return None

        if webpage_match and uri_filename_match:
            uri = webpage.replace(webpage_match.group(1), uri_filename_match.group(1))

        # Asignando el protocolo https para obtener un objeto correcto para el módulo requests
        if "http" not in uri or "https" not in uri:
            uri = "https://" + uri

        return uri

    def _scraper(self, website):
        try:
            headers = {
                'User-Agent': UserAgent().chrome
            }

            # Si website tiene un / al final, se le quita
            website = website[:len(website) - 1] if website[len(website) - 1] == "/" else website

            domain = Node._get_domain(website)

            if domain is None:
                raise Exception("No se pudo obtener dominio")

            r = requests.get(website, headers=headers)

            soup = BeautifulSoup(r.content, 'lxml')
            links = []

            for link in soup.find_all('a', href=True):
                uri = link.get('href')
                uri = Node._uri_cleaner(uri, domain, website)

                if uri is not None and uri not in links and uri != website:
                    if uri not in Node.visited:
                        links.append(uri)
                        Node.visited.append(uri)

            return links
        except Exception as e:
            raise Exception(e)
