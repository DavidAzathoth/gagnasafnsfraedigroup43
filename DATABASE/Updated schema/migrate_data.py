# Task C4
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/OrkuflaediIsland"

def migrate_data():
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        

        connection.execute(text("""
            INSERT INTO raforka_updated.eigendur_notenda (kennitala, heiti)
            SELECT DISTINCT kennitala, eigandi
            FROM raforka_legacy.notendur_skraning
            WHERE kennitala IS NOT NULL
                AND eigandi IS NOT NULL
"""))

        



if __name__ == "__main__":
    migrate_data()