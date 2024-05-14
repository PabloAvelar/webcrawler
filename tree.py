from node import Node
from sumario import get_sumario
from sumario import scrape_sumario
from cache import cache
from cache import set_new_records


class Tree:
    def __init__(self):
        self._root = None
        self._counter = 0

    def search_cache(self, **kwargs):
        keywords = []
        for key, value in kwargs.items():
            if key == 'keywords':
                keywords = value.split(",")

        records = cache(keywords)
        if len(records) > 0:
            self.print_records(records)
        else:
            print("No hay coincidencias.")
        return


    def build(self, website: str, **kwargs):
        """
        Función para armar un árbol de la estructura del sitio web
        :arg website -> str
        :return None
        """

        if website == "":
            return

        keywords = []
        use_sumario = False
        use_cache = True

        for key, value in kwargs.items():
            if key == 'keywords':
                keywords = value.split(",")
            if key == 'sumario':
                use_sumario = value
            if key == 'cache':
                use_cache = value

        if use_sumario:
            sumario = get_sumario(website)
            if sumario is not None:
                scrape_sumario(sumario, keywords)

            return

        # Checando en caché y evitar hacer todo el proceso otra vez
        if use_cache:
            records = cache(keywords)
            if len(records) > 0:
                self.print_records(records)
            else:
                print("No hay coincidencias.")
            return

        # Creando el nodo raíz
        self._root = Node(parent=None, children=None, page=website)
        self._root.read_robots(website)
        if len(keywords) > 0:
            self._root.set_keywords(keywords)

            self._root.crawl(self._root)

        print("Imprimiendo el árbol...")
        self.print()


    @staticmethod
    def print_records(records) -> None:
        """
        Función para mostrar las coincidencias en el caché, la base de datos
        :param records: list of tuples
        :return: None
        """

        for record in records:
            print("\t", record[1])
            print(record[2])
            print("------------------------")

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

    @staticmethod
    def results():
        # Guardando esta nueva coincidencia en caché!!!
        set_new_records(list(Node.search))

        for result in Node.search:
            print("\t", result[0])
            print(result[1])
            print("--------")


