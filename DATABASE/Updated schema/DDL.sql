-- Task C3

DROP TABLE IF EXISTS raforka_updated.eiganda_skraning
DROP TABLE IF EXISTS notendur_skraning
DROP TABLE IF EXISTS orku_einingar
DROP TABLE IF EXISTS orku_maelingar

--
-- Name: raforka_; Type: SCHEMA; Schema: -; Owner: bjarki1312
--
CREATE SCHEMA raforka_updated;


CREATE TABLE raforka_updated.eigendur_notenda (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kennitala CHAR(10) UNIQUE NOT NULL,
    heiti VARCHAR(100) NOT NULL,

    CHECK(kennitala ~ '^[0-9]{10}$')
);

CREATE TABLE raforka_updated.notendur_skraning (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    ar_stofnad integer NOT NULL,
    "X_HNIT" double precision,
    "Y_HNIT" double precision,
    eigandi_id integer,

    CHECK(ar_stofnad >= 1900 AND ar_stofnad <= EXTRACT(YEAR FROM CURRENT_DATE)),

    FOREIGN KEY(eigandi_id)
        REFERENCES raforka_updated.fyrirtaeki_skraning(id)
);


CREATE TABLE raforka_updated.orku_einingar (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    tegund VARCHAR(100) NOT NULL,
    eigandi VARCHAR(100) NOT NULL,
    ar_uppsett date NOT NULL,
    "X_HNIT" decimal(9, 6) NOT NULL,
    "Y_HNIT" decimal(9, 6) NOT NULL,
    tengd_stod int,
    FOREIGN KEY (tengd_stod) REFERENCES orku_einingar(id)
);

CREATE TABLE raforka_updated.stodvar (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

);

CREATE TABLE raforka_updated.virkjanir (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
)


CREATE TABLE raforka_updated.orku_maelingar (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    eining_id int NOT NULL REFERENCES orku_einingar(id),
    tegund VARCHAR(11) CHECK (
        LOWER(tegund) IN ('framleiðsla', 'innmötun', 'úttekt')),
    sendandi_maelingar text,
    timi timestamp without time zone,
    gildi_kwh numeric,
    notandi_heiti text
);

CREATE TABLE raforka_updated.uttekt (
    maeling_id integer PRIMARY KEY REFERENCES orku_maelingar(id),
    notandi_heiti VARCHAR(100) NOT NULL,

);

CREATE TABLE raforka_updated.framleidsla (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maeling_id integer REFERENCES orku_maelingar(id),
    virkjun_id integer NOT NULL REFERENCES orku_einingar(id)
);

CREATE TABLE raforka_updated.innmotun (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    maeling_id integer PRIMARY KEY REFERENCES orku_maelingar(id),
    stod integer NOT NULL REFERENCES orku_einingar(id)
);

-- Task D1