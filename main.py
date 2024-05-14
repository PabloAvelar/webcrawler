from tree import Tree
from multiprocessing import Process, Manager


def get_websites():
    """
    Devuelve la lista de sitios web a explorar

    :return:
    """

    return [
        'https://www.scjn.gob.mx/',
        'https://dof.gob.mx/'
    ]


def main():
    manager = Manager()
    shared_list = manager.list()
    pages_tree = Tree(shared_list)

    # website = input("Ingresa la URL del sitio web: ")
    # website = "https://www.scjn.gob.mx/"

    option = int(input("""
                Web Crawler de Pablo y Ricardo!
        
        1) Búsqueda con caché
        2) Búsqueda exhaustiva
        
        : """))

    keywords = input("Ingresa palabras clave a buscar: ")

    if option == 1:
        print("Búsqueda con caché...")
        pages_tree.search_cache(keywords=keywords)
    elif option == 2:
        print("Búsqueda exhaustiva: explorando el sitio...")

        # Creando procesos para cada sitio web
        processes = []

        for website in get_websites():
            process = Process(target=pages_tree.build, args=(website, ), kwargs={'keywords': keywords, 'cache': False})
            process.start()
            processes.append(process)

        # Esperar a que cada proceso termine
        for process in processes:
            process.join()

        print("Resultados de la búsqueda")
        pages_tree.results()

        # pages_tree.build(website, keywords=keywords, cache=False)


if __name__ == '__main__':
    main()
