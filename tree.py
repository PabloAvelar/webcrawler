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
                keywords.append(value.split(","))

        if website != "":
            # Creando el nodo raíz
            self._root = Node(parent=None, children=None, page=website)
            self._root.read_robots(website)
            if len(keywords) > 0:
                self._root.set_keywords(keywords)

            self._root.crawl(self._root)

    def print(self):
        Node.print_tree(tree=self._root, level=0)

    def results(self):
        print(Node.search)