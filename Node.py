import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning

class Node:
    # Atributo de clase para memoria dinámica y evitar bucles infinitos
    visited = []
    forms_action = []

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
        file_re = r'.*\.(docx|doc|pdf|xls)$'
        file_match = re.search(file_re, tree.page)

        if file_match:
            return None

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

        if "#" in uri or 'javascript' in uri:
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
        #         else:
        #             uri = f'{webpage}/{uri}' if uri[0] != '/' else domain+uri
        # Si el link es de una página externa
        elif uri_domain != domain:
            return None

        #     if webpage_match and uri_filename_match:
        #         uri = webpage.replace(webpage_match.group(1), uri_filename_match.group(1))
        #         return uri

        # Asignando el protocolo https para obtener un objeto correcto para el módulo requests
        if "http" not in uri and "https" not in uri:
            uri = "https://" + uri

            # Verificando que la URI sea correcta
        #     try:
        #         response = requests.get(uri)
        #         if response.status_code == 404:
        #             return None
        #     except:
        #         return None

        # Quitando el / del final
        if uri[len(uri) - 1] == '/':
            uri = uri[:-1]

        return uri

    def _scraper(self, website):
        try:
            headers = {
                'User-Agent': UserAgent().chrome
            }

            # Si website tiene un / al final, se le quita
            website = website[:len(website) - 1] if website[len(website) - 1] == "/" else website
            Node.visited.append(website)

            domain = Node._get_domain(website)

            if domain is None:
                raise Exception("No se pudo obtener dominio")

            r = None
            try:
                r = requests.get(website, headers=headers)
            except requests.exceptions.SSLError:
                # print("No se pudo verificar SSL")
                r = requests.get(website, headers=headers, verify=False)
                requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            except Exception as e:
                print("Error en la petición GET")
                return None

            soup = BeautifulSoup(r.content, 'lxml')
            links = []

            for link in soup.find_all('a', href=True):

                uri = link.get('href')

                if len(uri) == 0:
                    continue

                uri = Node._uri_cleaner(uri, domain, website)

                if uri is not None and uri not in links and uri != website:
                    if uri not in Node.visited:
                        links.append(uri)
                        Node.visited.append(uri)

            return links
        except Exception as e:
            raise Exception(e)
