import pandas as pd
import psycopg2

import os
from dotenv import load_dotenv
# Ne fonctionne pas pour l'instant
# Preferer utiliser directement une requete SQL

load_dotenv()
# Connexion a la base de donnée locale
conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

TABLE = os.getenv("DB_TABLE")

cur = conn.cursor()

print("Execution de la requete SQL")
cur.execute("""
    SELECT yticker, date, px_last, px_high, px_low, px_open, px_volume, meta
    FROM {} AS t
    LEFT JOIN lexique AS l
        ON yticker = yf_ticker
    WHERE l.meta
    ORDER BY date DESC
    """.format(TABLE))

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
df.to_excel("{}.xlsx".format(TABLE))
