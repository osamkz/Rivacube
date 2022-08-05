from tokenize import String
import time
import psycopg2

# Connexion a la base de donnée locale
conn = psycopg2.connect(database='slm', user='postgres',
                        host='127.0.0.1', port='5432')


def request(req: String) -> None:
    start_request = time.time()
    cur = conn.cursor()

    cur.execute(req)
    end_request = time.time()

    start_fetch = time.time()
    elements = len(cur.fetchall())
    end_fetch = time.time()

    cur.close()

    print("""
        Requete: {}
        Temps de la requete:        {:.0f}ms
        Temps de la recuperation:   {:.0f}ms
        Temps total:                {:.0f}ms
        Nombre d'elements:          {}
    """.format(
        req,
        (end_request - start_request) * 1000,
        (end_fetch - start_fetch) * 1000,
        (end_fetch - start_request) * 1000,
        elements
    ))


REQUESTS = [
    "SELECT * FROM main WHERE yticker='AAPL' AND EXTRACT(YEAR FROM date) = 2021",
    "SELECT * FROM main WHERE yticker='AAPL' AND EXTRACT(YEAR FROM date) <= 2021 AND EXTRACT(YEAR FROM date) > 2011",
    "SELECT * FROM main WHERE yticker='AAPL'",
    "SELECT * FROM main WHERE date >= '2021-01-01' AND date <= '2021-12-31'",
    "SELECT * FROM main WHERE date >= '2012-01-01' AND date <= '2021-12-31'",
    "SELECT * FROM main",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.ccy='EUR'",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.ccy='EUR' AND EXTRACT(YEAR FROM main.date) = 2021",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.ccy='EUR' AND date >= '2021-01-01' AND date <= '2021-12-31'",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.sector='Consumer, Cyclical'",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.sector='Consumer, Cyclical' AND lexique.gics_sub_sector = 'Casinos & Gaming'",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.id_zone = 'US'",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.country = 'FRANCE'",
    "SELECT * FROM main JOIN lexique ON main.yticker = lexique.yf_ticker WHERE lexique.nikkei"
]

for r in REQUESTS:
    request(r)

conn.close()
