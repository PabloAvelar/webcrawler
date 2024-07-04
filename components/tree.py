from components.node import Node
from utils.sumario import get_sumario
from utils.sumario import scrape_sumario
from utils.cache import cache
from utils.cache import set_new_records


class Tree:
    def __init__(self, shared_list):
        self._root = None
        self._counter = 0
        self._shared_list = shared_list

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

        self._shared_list.extend(Node.search)
        # print("Imprimiendo el árbol...")
        # self.print()


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

    def results(self):
        """
        Muestra resultados de la busqueda por keywords.
        El orden de indexacion es:
            h1 - (nombres de clase)
            h2
            h3
            h4
            h5
            p
            a
            li
            table-data
        """
        # Guardando esta nueva coincidencia en caché!!!
        set_new_records(tuple(self._shared_list))

        # Crear un diccionario para almacenar los resultados organizados por etiquetas
        results_by_tag = {
            'h1': [], # Aquí también va "txt_blanco"
            'h2': [], # Aquí también va "enlaces" y "enlaces_leido"
            'h3': [],
            'h4': [],
            'h5': [],
        }

        # Organizar los resultados por etiqueta
        for result in self._shared_list:
            text, website, tag_name = result

            tag_name = 'h1' if tag_name == 'txt_blanco' else tag_name
            tag_name = 'h2' if tag_name == 'enlaces' or tag_name == 'enlaces_leido' else tag_name

            # Asegurarse de manejar la etiqueta 'table-data'
            if tag_name in results_by_tag:
                results_by_tag[tag_name].append((text, website))

        # Imprimir los resultados ordenados por etiquetas
        for tag_name in ['h1', 'h2', 'h3', 'h4', 'h5']:
            if len(tag_name) == 0:
                continue

            try:
                for text, website in results_by_tag[tag_name]:
                    print("\t", text)
                    print("\t", website)
                print("--------")
            except KeyError:
                pass

