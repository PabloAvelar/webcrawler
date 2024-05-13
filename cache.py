from connection import connection

cur = connection()


def cache(*args):
    query = "SELECT * FROM search"
    cur.execute(query)

    return cur.fetchall()


data = cache()
keywords = ["méxico"]
results = []

for row in data:
    for kw in keywords:
        if kw in row[1].lower():
            results.append(row)


print("Resultados:")
for result in results:
    print("\t" + result[1])
    print(result[2])