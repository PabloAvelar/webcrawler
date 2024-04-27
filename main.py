from tree import Tree


def main():
    pages_tree = Tree()

    print("\tWEB CRAWLER\n")
    website = input("Ingresa la URL del sitio web: ")

    print("Construyendo el árbol...")
    pages_tree.build(website)

    print("Imprimiendo el árbol...")
    pages_tree.print()


if __name__ == '__main__':
    main()
