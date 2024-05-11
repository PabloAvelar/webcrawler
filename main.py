from tree import Tree


def main():
    pages_tree = Tree()

    print("\tWEB CRAWLER\n")
    website = input("Ingresa la URL del sitio web: ")

    keywords = input("Ingresa palabras clave a buscar: ")

    print("Construyendo el árbol...")
    pages_tree.build(website, keywords=keywords)

    print("Imprimiendo el árbol...")
    pages_tree.print()

    print("Resultados de la búsqueda")
    pages_tree.results()


if __name__ == '__main__':
    main()
