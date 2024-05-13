from connection import connection

conn = connection()

def cache(keywords: list) -> tuple:
    """s
    Función para buscar información con palabras clave en la base de datos como caché.

    Recibe: list -> Lista de palabras clave para buscar
    Devuelve: tuple -> Tupla con las coincidencias de la búsqueda con palabras clave en la base de datos

    """
    cur = conn.cursor()

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


def set_new_records(records: list) -> None:
    """
    Función para insertar nuevos registros para el caché del webcrawler
    :param records: list
    :return: None
    """
    cur = conn.cursor()

    base_query = """
        INSERT INTO `search` (description, link, html_origin)
        VALUES (%s, %s, %s)                
    """

    try:
        cur.executemany(base_query, records)
        conn.commit()  # Confirmar la transacción
    except Exception as e:
        print(f"Error inserting records: {e}")
