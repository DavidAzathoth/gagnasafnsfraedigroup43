# Task C4
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:123@localhost:5432/OrkuflaediIsland"

def migrate_data():
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        

        connection.execute(text("""
            ....
"""))

        



if __name__ == "__main__":
    migrate_data()