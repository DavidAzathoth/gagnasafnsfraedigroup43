# Task C4
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/OrkuflaediIsland"

def migrate_data():
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
##########Migrate eigendur_eininga############
        connection.execute(text("""
            INSERT INTO raforka_updated.eigendur_eininga (heiti)
            SELECT DISTINCT(oe.eigandi)
            FROM raforka_legacy.orku_einingar oe;
"""))
        
############Migrate orku_einingar############
        connection.execute(text("""
            CREATE TEMP TABLE id_map (
                old_id INT,
                new_id INT
        );
"""))
        connection.execute(text("""
            INSERT INTO raforka_updated.orku_einingar
            (heiti, tegund, ar_uppsett, "X_HNIT", "Y_HNIT")
            SELECT
                heiti,
                tegund,
                MAKE_DATE(ar_uppsett, manudir_uppsett, dagur_uppsett),
                CAST("X_HNIT" AS DECIMAL(9,6)),
                CAST("Y_HNIT" AS DECIMAL(9,6))
            FROM raforka_legacy.orku_einingar;
"""))
        connection.execute(text("""
            INSERT INTO id_map (old_id, new_id)
            SELECT old.id, new.id
            FROM raforka_legacy.orku_einingar old
            JOIN raforka_updated.orku_einingar new
            ON old.heiti = new.heiti;
"""))
        connection.execute(text("""
            UPDATE raforka_updated.orku_einingar new
            SET tengd_stod = m2.new_id
            FROM raforka_legacy.orku_einingar old
            JOIN id_map m1 ON old.id = m1.old_id

            LEFT JOIN raforka_legacy.orku_einingar ref
                ON old.tengd_stod = ref.heiti

            LEFT JOIN id_map m2
                ON ref.id = m2.old_id

            WHERE new.id = m1.new_id;
"""))
        connection.execute(text("""
            UPDATE raforka_updated.orku_einingar new
            SET eigandi_id = e.id
            FROM id_map m
            JOIN raforka_legacy.orku_einingar old ON old.id = m.old_id
            JOIN raforka_updated.eigendur_eininga e ON e.heiti = old.eigandi 
            WHERE new.id = m.new_id;
"""))
        connection.execute(text("""
            INSERT INTO raforka_updated.stodvar
            (id, tegund)
            SELECT
                id,
                tegund
            FROM
            raforka_updated.orku_einingar e
            WHERE e.tegund = 'stod'
"""))
        connection.execute(text("""
            INSERT INTO raforka_updated.virkjanir
            (id, tegund)
            SELECT
                id,
                tegund
            FROM
            raforka_updated.orku_einingar e
            WHERE e.tegund = 'virkjun'
"""))



if __name__ == "__main__":
    migrate_data()