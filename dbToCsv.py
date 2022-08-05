import pandas as pd
import psycopg2

# Ne fonctionne pas pour l'instant
# Preferer utiliser directement une requete SQL

# Connexion a la base de donnée locale
conn = psycopg2.connect(database='slm', user='postgres',
                        host='127.0.0.1', port='5432')

TABLE = 'ticker_ticker'

cur = conn.cursor()

print("Execution de la requete SQL")
cur.execute("""
    SELECT yticker, date, px_last, px_high, px_low, px_open, px_volume, meta
    FROM ticker_ticker AS t
    LEFT JOIN lexique AS l
        ON yticker = yf_ticker
    WHERE l.meta
    ORDER BY date DESC
    """)

print("Recuperation des données depuis la base en cours")
data = cur.fetchall()

print("Transformation des donnée en Dataframe")
df = pd.DataFrame(data)
df.columns = ["Ticker", "Date", "Last",
              "High", "Low", "Open", "Volume", "Meta"]

print("Modification du type des données")
for col in ["Last", "High", "Low", "Open"]:
    df[col] = df[col].astype(float)

print("Creation du csv")
df.to_excel("ticker_ticker.xlsx")
