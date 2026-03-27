-- Task C3


DROP TABLE IF EXISTS
    raforka_updated.eigendur_notenda,
    raforka_updated.notendur_skraning,
    raforka_updated.orku_einingar,
    raforka_updated.stodvar,
    raforka_updated.virkjanir,
    raforka_updated.orku_maelingar,
    raforka_updated.uttekt,
    raforka_updated.framleidsla,
    raforka_updated.innmotun


--
-- Name: raforka_; Type: SCHEMA; Schema: -; Owner: bjarki1312
--
CREATE SCHEMA raforka_updated;


CREATE TABLE raforka_updated.eigendur_notenda (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kennitala CHAR(10) UNIQUE NOT NULL,
    heiti VARCHAR(100) NOT NULL,

    CHECK(kennitala ~ '^[0-9]{10}$')
);

CREATE TABLE raforka_updated.notendur_skraning (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    ar_stofnad int NOT NULL,
    "X_HNIT" decimal(9, 6) NOT NULL,
    "Y_HNIT" decimal(9, 6) NOT NULL,
    eigandi_id int REFERENCES raforka_updated.eigendur_notenda(id),

    CHECK(ar_stofnad >= 1900 AND ar_stofnad <= EXTRACT(YEAR FROM CURRENT_DATE)),
);


CREATE TABLE raforka_updated.orku_einingar (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    tegund VARCHAR(7) NOT NULL CHECK(LOWER(tegund) IN ('stod', 'virkjun')),
    eigandi VARCHAR(100) NOT NULL,
    ar_uppsett date NOT NULL,
    "X_HNIT" decimal(9, 6) NOT NULL,
    "Y_HNIT" decimal(9, 6) NOT NULL,
    tengd_stod int NULL,
    FOREIGN KEY (tengd_stod) REFERENCES raforka_updated.orku_einingar(id)
);

CREATE TABLE raforka_updated.stodvar (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY

);

CREATE TABLE raforka_updated.virkjanir (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);


CREATE TABLE raforka_updated.orku_maelingar (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    eining_id int NOT NULL REFERENCES raforka_updated.orku_einingar(id),
    tegund VARCHAR(11) CHECK (
        LOWER(tegund) IN ('framleiðsla', 'innmötun', 'úttekt')),
    timi timestamp without time zone,
    gildi_kwh numeric,
    notandi_id int REFERENCES raforka_updated.notendur_skraning(id),
    stod int REFERENCES raforka_updated.orku_einingar(id)
);


/*delete this*/
CREATE TABLE raforka_updated.uttekt (
    maeling_id int PRIMARY KEY REFERENCES raforka_updated.orku_maelingar(id),
    notandi_id int NOT NULL REFERENCES raforka_updated.notendur_skraning(id)
);

CREATE TABLE raforka_updated.framleidsla (
    maeling_id int PRIMARY KEY REFERENCES raforka_updated.orku_maelingar(id),
    virkjun_id int NOT NULL REFERENCES raforka_updated.orku_einingar(id)
);

CREATE TABLE raforka_updated.innmotun (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maeling_id int NOT NULL REFERENCES raforka_updated.orku_maelingar(id),
    stod int NOT NULL REFERENCES raforka_updated.orku_einingar(id)
);


----------------------------------------------------------------
    --1
    CREATE TEMP TABLE id_map (
        old_id INT,
        new_id INT
    );


    --2
    INSERT INTO raforka_updated.orku_einingar
    (heiti, tegund, eigandi, ar_uppsett, "X_HNIT", "Y_HNIT")
    SELECT
        heiti,
        tegund,
        eigandi,
        MAKE_DATE(ar_uppsett, manudir_uppsett, dagur_uppsett),
        CAST("X_HNIT" AS DECIMAL(9,6)),
        CAST("Y_HNIT" AS DECIMAL(9,6))
    FROM raforka_legacy.orku_einingar
    RETURNING id;


    --3
    INSERT INTO id_map (old_id, new_id)
    SELECT old.id, new.id
    FROM raforka_legacy.orku_einingar old
    JOIN raforka_updated.orku_einingar new
    ON old.heiti = new.heiti;

    --4
    UPDATE raforka_updated.orku_einingar new
    SET tengd_stod = m2.new_id
    FROM raforka_legacy.orku_einingar old
    JOIN id_map m1 ON old.id = m1.old_id

    -- find the referenced row by name
    LEFT JOIN raforka_legacy.orku_einingar ref
        ON old.tengd_stod = ref.heiti

    -- map that referenced row to new_id
    LEFT JOIN id_map m2
        ON ref.id = m2.old_id

    WHERE new.id = m1.new_id;


select * 
from raforka_updated.orku_einingar;

select *
from raforka_legacy.orku_einingar;

select * 
from raforka_legacy.orku_maelingar
LIMIT 100;

-- Task D1