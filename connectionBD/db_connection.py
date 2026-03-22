import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# --> tahmil les variable dans .env
load_dotenv()

# --> enregistrer le contenu dans un variable
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "superstore_db")

# --> function de connection
def get_engine():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        return engine

    except Exception as e:
        print("Erreur connexion base :", e)
        return None