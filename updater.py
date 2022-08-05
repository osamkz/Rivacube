import datetime
import yfinance as yf
import pandas as pd
import time
import psycopg2
import enlighten


import os
from dotenv import load_dotenv

load_dotenv()
# Connexion a la base de donnée locale
conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

TABLE = os.getenv("DB_TABLE")


def create_table(file="ticker_ticker"):
    cur = conn.cursor()

    # Verification de l'existence de la table
    cur.execute("""
        SELECT *
        FROM pg_catalog.pg_tables
        WHERE tablename='{}'
    """.format(file))

    if cur.fetchone():
        print("La table {} existe déjà".format(file))
        cur.close()
        return 0
    else:
        print("Création de la table {}".format(file))

    # Creation de la table
    cur.execute("""
        CREATE TABLE {}
            (
                id VARCHAR(20) PRIMARY KEY,
                yticker VARCHAR(12) REFERENCES lexique(yf_ticker),
                date DATE,
                px_LAST FLOAT,
                PX_HIGH FLOAT,
                PX_LOW FLOAT,
                PX_OPEN FLOAT,
                PX_VOLUME BIGINT
            );
    """.format(file))

    conn.commit()
    cur.close()


def create_lexique_and_return_all_tickers():
    cur = conn.cursor()

    # Verification de l'existence de la table
    cur.execute("""
        SELECT *
        FROM pg_catalog.pg_tables
        WHERE tablename='lexique'
    """)

    if cur.fetchone():
        print("La table lexique existe déjà")
        cur.close()
        return 0
    else:
        print("Création de la table lexique")

    # Creation de la table
    cur.execute("""
        DROP TYPE IF EXISTS SECTEUR;
        CREATE TYPE SECTEUR AS ENUM (
            'Basic Materials',
            'Communications',
            'Consumer, Cyclical',
            'Consumer, Non-cyclical',
            'Diversified',
            'Energy',
            'Financial',
            'Industrial',
            'Technology',
            'Utilities'
        );

        CREATE TABLE lexique
            (
                isin VARCHAR(12) UNIQUE,
                bbg_ticker VARCHAR(14) UNIQUE,
                yf_ticker VARCHAR(12) PRIMARY KEY,
                name VARCHAR(100),
                sector SECTEUR,
                gics_sub_sector VARCHAR(100),
                id_zone VARCHAR(2),
                country VARCHAR(15),
                ccy VARCHAR(3),
                adr BOOLEAN,
                indu BOOLEAN,
                ndx BOOLEAN,
                spx BOOLEAN,
                tsx BOOLEAN,
                sxxp BOOLEAN,
                ftsie BOOLEAN,
                spi BOOLEAN,
                nikkei BOOLEAN,
                kospi BOOLEAN,
                hangseng BOOLEAN,
                australia BOOLEAN,
                no_index BOOLEAN,
                cybersecurity BOOLEAN,
                petsfervor BOOLEAN,
                biodefense BOOLEAN,
                adv_mat BOOLEAN,
                meta BOOLEAN,
                ltp BOOLEAN
            );
    """)

    conn.commit()

    # Création d'un dataframe pour la requete
    df = pd.DataFrame(pd.read_excel(
        "/home/ubuntu/python_code/RivaLexique.xlsx"))
    df.drop([543, 544, 546, 547, 551, 567, 577, 711, 712, 713, 1530, 2203], inplace=True,
            axis=0)  # CNP, CMS, PEG, FE, SRE, SRNE, CERS, CA09228F1036, CA12532H1047, CA82509L1076, IE00BZ12WP82, GB0005405286
    df.fillna(0, inplace=True)
    df["ADR"] = df["ADR"].astype(bool)
    df["INDU"] = df["INDU"].astype(bool)
    df["NDX"] = df["NDX"].astype(bool)
    df["SPX"] = df["SPX"].astype(bool)
    df["TSX"] = df["TSX"].astype(bool)
    df["SXXP"] = df["SXXP"].astype(bool)
    df["FTSIE"] = df["FTSIE"].astype(bool)
    df["SPI"] = df["SPI"].astype(bool)
    df["NIKKEI"] = df["NIKKEI"].astype(bool)
    df["KOSPI"] = df["KOSPI"].astype(bool)
    df["HangSeng"] = df["HangSeng"].astype(bool)
    df["Australia"] = df["Australia"].astype(bool)
    df["No Index"] = df["No Index"].astype(bool)
    df["Cybersecurity"] = df["Cybersecurity"].astype(bool)
    df["PetsFervor"] = df["PetsFervor"].astype(bool)
    df["Biodefense"] = df["Biodefense"].astype(bool)
    df["Adv Mat"] = df["Adv Mat"].astype(bool)
    df["Meta"] = df["Meta"].astype(bool)
    df["LTP"] = df["LTP"].astype(bool)
    df.loc[(df["BBG Ticker"] == 'UAA UN'), 'YF Ticker'] = 'UAA'
    df.loc[(df["BBG Ticker"] == 'PMAG SE'), 'YF Ticker'] = 'PMAG.SW'

    # Importation des données
    for row in df.itertuples():
        cur.execute("""
            INSERT INTO lexique
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s)
            """,
                    [
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                        row[12],
                        row[13],
                        row[14],
                        row[15],
                        row[16],
                        row[17],
                        row[18],
                        row[19],
                        row[20],
                        row[21],
                        row[22],
                        row[23],
                        row[24],
                        row[25],
                        row[26],
                        row[27],
                        row[28]
                    ]
                    )

    conn.commit()

    cur.close()

    # Selection des valeurs de la colonne isin et conversion en array
    return df['YF Ticker'].values


def get_data_from_ticker(ticker: str, period: str = "1970-01-01") -> pd.DataFrame:
    data = yf.Ticker(ticker).history(start=period)
    return data


def add_file_to_database(data: pd.DataFrame, ticker: str) -> None:
    # Transformation de l'index (Date) en colonne
    data['date'] = data.index
    data.dropna(inplace=True)

    # Suppression des lignes contenant des dates dupliquées, en ne gardant que la premiere
    # data.drop_duplicates(subset='date', keep='first')

    cur = conn.cursor()

    # Importation des données
    for row in data.itertuples():
        try:
            cur.execute("""
                INSERT INTO {} (id, yticker, date, px_last, px_high, px_low, px_open, px_volume)
                VALUES ('{}','{}','{}',{},{},{},{},{})
                """.format(
                TABLE,
                ticker +
                "{:0>4d}{:0>2d}{:0>2d}".format(
                    row.date.year, row.date.month, row.date.day),
                ticker,
                row.date,
                row.Close,
                row.High,
                row.Low,
                row.Open,
                row.Volume
            )
            )
        except psycopg2.errors.UniqueViolation as e:
            conn.rollback()
            print("L'importation de {} à la date de {} a echoué.\nRaison: {}".format(
                ticker, row.date, e))

    conn.commit()
    cur.close()


def get_all_tickers_and_last_date():
    cur = conn.cursor()

    cur.execute("""
        SELECT yticker, MAX(date)
        FROM {}
        GROUP BY yticker
    """.format(TABLE))

    return cur.fetchall()


# Recupere les tickers et dates depuis la base
# Filtre pour ne garder que ceux n'ayant pas ete mis a jour aujourd'hui (Pour ne pas recuperer 2 fois les memes valeurs)
ticker_date = list(
    filter(lambda x: x[1] < datetime.date.today() - datetime.timedelta(days=1), get_all_tickers_and_last_date()))

s = time.time()
with enlighten.Counter(total=len(ticker_date), desc="", unit="ticker") as pbar:
    for ticker, da in ticker_date:
        add_file_to_database(get_data_from_ticker(
            ticker, (da + datetime.timedelta(days=1, hours=1)).strftime('%Y-%m-%d')), ticker)
        pbar.update()
e = time.time()

t = e - s
time_per_file = t / len(ticker_date)
print("Récupérations effectuées en {:.2f}s ({:.2f}s par fichier)".format(
    t, time_per_file))

cur = conn.cursor()

conn.commit()
cur.close()
conn.close()
