from utils.connection import connection

conn = connection()

def cache(keywords: list) -> tuple:
    """
    Función para buscar información con palabras clave en la base de datos como caché.

    :argument keywords: Lista de palabras clave para buscar
    :return tuple: Tupla con las coincidencias de la búsqueda con palabras clave en la base de datos

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


def set_new_records(records: tuple) -> None:
    """
    Función para insertar nuevos registros para el caché del webcrawler
    :param records: list
    :return: None
    """
    cur = conn.cursor()

    base_query = """
        INSERT IGNORE INTO `search` (description, link, html_origin)
        VALUES (%s, %s, %s)                
    """

    try:
        cur.executemany(base_query, records)
        conn.commit()  # Confirmar la transacción
    except Exception as e:
        print(f"Error inserting records: {e}")
