# N'a servi que pour la creation initiale de la table ticker, ne devrait pas servir a nouveau

import os
import psycopg2
import pandas as pd
import time

from sshtunnel import SSHTunnelForwarder

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


def get_all_files():
    return os.listdir(os.getcwd() + "/CSV_Test")


def create_table(file="ticker_ticker"):
    cur = conn.cursor()

    # Verification de l'existence de la table
    cur.execute("""
        SELECT *
        FROM pg_catalog.pg_tables
        WHERE tablename='{0}'
    """.format(file))

    if cur.fetchone():
        print("La table {0} existe déjà".format(file))
        cur.close()
        return 0
    else:
        print("Création de la table {0}".format(file))

    # Creation de la table
    cur.execute("""
        CREATE TABLE {0}
            (
                id VARCHAR(20) PRIMARY KEY,
                isin VARCHAR(12),
                date DATE,
                px_last FLOAT,
                PX_HIGH FLOAT,
                PX_LOW FLOAT,
                PX_OPEN FLOAT,
                PX_VOLUME INTEGER
            )
    """.format(file))

    conn.commit()
    cur.close()


def add_file_to_database(file):
    if file == ".DS_Store":
        return

    isin = file.replace(".csv", "")

    cur = conn.cursor()

    # Recupération des données pour vérification
    cur.execute("""
        SELECT *
        FROM ticker_ticker
        WHERE isin='{}'
    """.format(isin))

    # Vérification de l'existence des données
    if cur.fetchone():
        print("Les données de {0} ont déjà été importées".format(isin))
        cur.close()
        return 0
    else:
        print("Importation des données de {0}".format(isin))

    # Création d'un dataframe pour la requete
    data = pd.read_csv(r'./CSV_TEST/{0}'.format(file))
    df = pd.DataFrame(data)

    # Importation des données
    for row in df.itertuples():
        cur.execute("""
            INSERT INTO ticker_ticker (id, isin, date, px_last, px_high, px_low, px_open, px_volume)
            VALUES ('{}','{}','{}',{},{},{},{},{})
            """.format(
            isin +
            row[1].split("-")[0] +  # Année
            row[1].split("-")[1] +  # Mois
            row[1].split("-")[2],  # Jour
            isin,
            row[1],
            row.PX_LAST,
            row.PX_HIGH,
            row.PX_LOW,
            row.PX_OPEN,
            row.PX_VOLUME
        )
        )

    conn.commit()


def test_select(titre):
    cur = conn.cursor()

    s = time.time()
    cur.execute("""
        SELECT *
        FROM ticker_ticker
        WHERE isin = '{}' AND EXTRACT(YEAR FROM date) = 2022
    """.format(titre))
    e = time.time()

    print(cur.fetchall())
    print("Selection effectuée en {:2f}s".format(e - s))


def test_select_all_count():
    cur = conn.cursor()

    s = time.time()
    cur.execute("""
        SELECT COUNT(*)
        FROM ticker_ticker
    """)
    e = time.time()

    print(cur.fetchall())
    print("Selection effectuée en {:2f}s".format(e - s))


create_table()

values = len(get_all_files())

s = time.time()
for i, file in enumerate(get_all_files()):
    print("{} sur {} ({}%)".format(i + 1, values, (i+1) * 100 / values))
    add_file_to_database(file)
e = time.time()

t = e - s
time_per_file = t / values

print("Importations effectuées en {:.2f}s ({:.2f}s par fichier, {:.2f} minutes pour 1500)".format(
    t, time_per_file, time_per_file * 25))

conn.close()
