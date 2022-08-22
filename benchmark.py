import time

from _modules.ConnectionManager import ConnectionManager


def request(req) -> None:
    start_request = time.time()
    cur = man.conn.cursor()

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


if __name__ == '__main__':
    REQUESTS = [
        ["SELECT * FROM ticker_ticker WHERE yticker='AAPL'",
            "Toutes les données de AAPL"],
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

    man = ConnectionManager('remote')

    for r in REQUESTS:
        request(r)

    man.close()
