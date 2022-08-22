import time
import psycopg2
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les informations depuis le fichier .env

PORT = int(os.getenv("PORT"))
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_SSH_PORT = int(os.getenv("REMOTE_SSH_PORT"))
REMOTE_USERNAME = os.getenv("REMOTE_USERNAME")
SSH_PASSWORD = os.getenv("SSH_KEY_PASSWORD")
SSH_PKEY = os.getenv("SSH_PKEY")

# Creation d'un tunnel SSH pour accéder a la base de donnée distante
server = SSHTunnelForwarder(
    (REMOTE_HOST, REMOTE_SSH_PORT),
    ssh_username=REMOTE_USERNAME,
    ssh_pkey=SSH_PKEY,
    ssh_private_key_password=SSH_PASSWORD,
    remote_bind_address=('localhost', PORT),
    local_bind_address=('localhost', PORT),
    compression=False)
server.start()

# Connexion a la base de donnée locale
conn = psycopg2.connect(database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
                        host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))


def request(req) -> None:
    start_request = time.time()
    cur = conn.cursor()

    cur.execute(req[0])
    end_request = time.time()

    start_fetch = time.time()
    elements = len(cur.fetchall())
    end_fetch = time.time()

    cur.close()

    print("""
        Requete: {}
        Traduction: {}
        Temps de la requete:        {:.0f}ms
        Temps de la recuperation:   {:.0f}ms
        Temps total:                {:.0f}ms
        Nombre d'elements:          {}
    """.format(
        req[0],
        req[1],
        (end_request - start_request) * 1000,
        (end_fetch - start_fetch) * 1000,
        (end_fetch - start_request) * 1000,
        elements
    ))


REQUESTS = [
    ["SELECT * FROM ticker_ticker WHERE yticker='AAPL'", "Toutes les données de AAPL"],
    ["SELECT * FROM ticker_ticker WHERE yticker='AAPL' AND EXTRACT(YEAR FROM date) = 2021",
     "Toutes les données de AAPL en 2021"],
    ["SELECT * FROM ticker_ticker WHERE date >= '2021-01-01' AND date <= '2021-12-31'",
        "Tous les tickers en 2021"],
    ["SELECT * FROM ticker_ticker WHERE date >= '2012-01-01' AND date <= '2021-12-31'",
        "Tous les tickers entre 2012 et 2022"],
    ["SELECT * FROM ticker_ticker", "Toute la base"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.ccy='EUR'",
        "Tous les tickers dont la monnaie est EUR"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.ccy='EUR' AND EXTRACT(YEAR FROM ticker_ticker.date) = 2021", "Tous les tickers dont la monnaie est EUR en 2021"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.ccy='EUR' AND date >= '2021-01-01' AND date <= '2021-12-31'",
        "Tous les tickers dont la monnaie est EUR en 2021"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.sector='Consumer, Cyclical'",
        "Tous les tickers dont le secteur est Consumer, Cyclical"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.sector='Consumer, Cyclical' AND ticker_lexique.gics_sub_sector = 'Casinos & Gaming'",
        "Tous les tickers dont le secteur est Consumer, Cyclical et le sous secteur est Casinos & Gaming"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.id_zone = 'US'",
        "Tous les tickers basés aux US"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.country = 'FRANCE'",
        "Tous les tickers basés en FRANCE"],
    ["SELECT * FROM ticker_ticker JOIN ticker_lexique ON ticker_ticker.yticker = ticker_lexique.yf_ticker WHERE ticker_lexique.market = 'NIKKEI'",
        "Tous les tickers cotés sur le Nikkei"]
]

for r in REQUESTS:
    request(r)

conn.close()
server.stop()
