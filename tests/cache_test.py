from connection import connection

conn = connection()

def cache(*args):
    cur = conn.cursor()
    query = "SELECT * FROM search"
    cur.execute(query)

    return cur.fetchall()


data = cache()
keywords = ["inglés"]
results = []

for row in data:
    for kw in keywords:
        if kw in row[1].lower():
            results.append(row)


if len(results) == 0:
    print("No hay coincidencias.")
else:
    print("Resultados:")
    for result in results:
        print("\t" + result[1])
        print(result[2])