from tree import Tree


def main():
    pages_tree = Tree()

    # website = input("Ingresa la URL del sitio web: ")
    website = "https://www.dof.gob.mx/"

    option = int(input("""
                Web Crawler de Pablo!
        
        1) Buscar por sumario
        2) Buscar por exploración del sitio
        
        : """))

    keywords = input("Ingresa palabras clave a buscar: ")

    if option == 1:
        print("Buscando por sumario...")
        pages_tree.build(website, keywords=keywords, sumario=True)
    elif option == 2:
        print("Explorando el sitio...")
        pages_tree.build(website, keywords=keywords)

        print("Imprimiendo el árbol...")
        pages_tree.print()

        print("Resultados de la búsqueda")
        pages_tree.results()


if __name__ == '__main__':
    main()
