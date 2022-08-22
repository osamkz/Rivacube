from dotenv import load_dotenv
import os
import psycopg2
import sshtunnel

from typing import Literal


class ConnectionManager:
    def __init__(self, type: Literal["local", "remote"] = "local") -> None:
        load_dotenv()  # Charge les information depuis le fichier .env

        # Adresse du serveur distant
        self.REMOTE_HOST = os.getenv("REMOTE_HOST")
        # Port SSH du serveur distant
        self.REMOTE_SSH_PORT = int(os.getenv("REMOTE_SSH_PORT"))
        # Nom d'utilisateur du serveur distant
        self.REMOTE_USERNAME = os.getenv("REMOTE_USERNAME")
        # Passphrase SSH
        self.SSH_PASSWORD = os.getenv("SSH_KEY_PASSWORD")
        # Emplacement de la cle SSH
        self.SSH_PKEY = os.getenv("SSH_PKEY")
        # Nom de la base de donnée
        self.DB_NAME = os.getenv("DB_NAME")
        # Nom d'utilisateur de la base de donnée
        self.DB_USER = os.getenv("DB_USER")
        # Adresse locale de la base de donnée
        self.DB_HOST = os.getenv("DB_HOST")
        # Port local de la base de donnée
        self.DB_PORT = int(os.getenv("DB_PORT"))

        # Type de connexion a utiliser: local ou remote
        self.type = type

        if self.type == "remote":
            self.server = self.start_server()

        self.conn = self.connect()

    # A la suppression de l'instance, lance la méthode close
    def __del__(self) -> None:
        self.close()

    # Ferme la connexion et stop le serveur si lancé
    def close(self) -> None:
        self.conn.close()
        print("La connexion à la base de donnée est interrompue")
        if self.type == "remote":
            self.server.stop()
            print("Le serveur est stoppé")

    # Connecte et renvoie psycopg2.extensions.connection
    def connect(self) -> psycopg2.extensions.connection:
        print("Connexion à la base de donnée en cours")
        c = psycopg2.connect(
            database=self.DB_NAME,
            user=self.DB_USER,
            host=self.DB_HOST,
            port=self.DB_PORT
        )
        print("Connexion a la base de donnée établie")
        return c

    # Demarre le serveur SSH
    def start_server(self) -> sshtunnel.SSHTunnelForwarder:
        print("Lancement du serveur")
        server = sshtunnel.SSHTunnelForwarder(
            (self.REMOTE_HOST, self.REMOTE_SSH_PORT),
            ssh_username=self.REMOTE_USERNAME,
            ssh_pkey=self.SSH_PKEY,
            ssh_private_key_password=self.SSH_PASSWORD,
            remote_bind_address=('localhost', self.DB_PORT),
            local_bind_address=('localhost', self.DB_PORT),
            compression=False)

        server.start()
        print("Le serveur est lancé")
        return server
