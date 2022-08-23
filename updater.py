# Sert a mettre a jour la base de donnée ticker quotidiennement

import datetime
import yfinance as yf
import pandas as pd
import time
import psycopg2
import enlighten

import os
import sys

from _modules.ConnectionManager import ConnectionManager


def get_data_from_ticker(ticker: str, period: str = "1970-01-01") -> pd.DataFrame:
    data = yf.Ticker(ticker).history(start=period)
    return data


def add_file_to_database(data: pd.DataFrame, ticker: str) -> None:
    # Transformation de l'index (Date) en colonne
    data['date'] = data.index
    data.dropna(inplace=True)

    # Suppression des lignes contenant des dates dupliquées, en ne gardant que la premiere
    # data.drop_duplicates(subset='date', keep='first')

    cur = man.conn.cursor()

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
            man.conn.rollback()
            print("L'importation de {} à la date de {} a echoué.\nRaison: {}".format(
                ticker, row.date, e))

    man.conn.commit()
    cur.close()


def get_all_tickers_and_last_date():
    cur = man.conn.cursor()

    cur.execute("""
        SELECT yticker, MAX(date)
        FROM {}
        GROUP BY yticker
    """.format(TABLE))

    return cur.fetchall()


if __name__ == "__main__":
    # Utilise le type envoyé en CLI si présent, sinon utilise remote
    man = ConnectionManager(sys.argv[1] if len(sys.argv) > 1 else "remote")

    TABLE = os.getenv("DB_TABLE")

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

    cur = man.conn.cursor()

    man.conn.commit()
    cur.close()
    man.close()
