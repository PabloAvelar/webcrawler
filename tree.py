from node import Node


class Tree:
    def __init__(self):
        self._root = None
        self._counter = 0

    """
    Función para armar un árbol de la estructura del sitio web
    
    Recibe: sitio web -> str
    Devuelve: Nada
    """
    def build(self, website:str, **kwargs):
        keywords = []
        for key, value in kwargs.items():
            if key == 'keywords':
                keywords = value.split(",")

        if website != "":
            # Creando el nodo raíz
            self._root = Node(parent=None, children=None, page=website)
            self._root.read_robots(website)
            if len(keywords) > 0:
                self._root.set_keywords(keywords)

            self._root.crawl(self._root)

    def print(self):
        Node.print_tree(tree=self._root, level=0)

    """
    Muestra resultados de la busqueda por keywords.
    El orden de indexacion es:
        h1
        h2
        h3
        h4
        class_names
    """
    def results(self):
        for result in Node.search:
            print(result['title'])
            print(result['link'])
            print("--------")