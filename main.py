from tree import Tree


def main():
    pages_tree = Tree()

    # website = input("Ingresa la URL del sitio web: ")
    website = "https://www.gob.mx/tramites/programas"

    option = int(input("""
                Web Crawler de Pablo y Ricardo!
        
        1) Búsqueda por sumario
        2) Búsqueda con caché
        3) Búsqueda exhaustiva
        
        : """))

    keywords = input("Ingresa palabras clave a buscar: ")

    if option == 1:
        print("Buscando por sumario...")
        pages_tree.build(website, keywords=keywords, sumario=True)
    elif option == 2:
        print("Búsqueda con caché...")
        pages_tree.build(website, keywords=keywords)
    elif option == 3:
        print("Búsqueda exhaustiva: explorando el sitio...")
        pages_tree.build(website, keywords=keywords, cache=False)


if __name__ == '__main__':
    main()
