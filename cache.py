from connection import connection

cur = connection()


def cache(keywords: list) -> tuple:
    """s
    Función para buscar información con palabras clave en la base de datos como caché.

    Recibe: list -> Lista de palabras clave para buscar
    Devuelve: tuple -> Tupla con las coincidencias de la búsqueda con palabras clave en la base de datos

    """

    base_query = """
    SELECT *
    FROM `search` s
    WHERE 
    """

    like_kw = ""
    for i in range(len(keywords)):
        like_kw += f'description LIKE "%{keywords[i]}%"'
        if i < len(keywords) - 1:
            like_kw += " or "

    query = base_query + like_kw + ";"

    cur.execute(query)

    return cur.fetchall()


keywords = ["justicia", "ley"]
print("resultados")
for x in cache(keywords):
    print(x)
