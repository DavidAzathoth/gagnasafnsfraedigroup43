-- Task C3

CREATE TABLE raforka_legacy.fyrirtaeki_skraning (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kennitala CHAR(10) UNIQUE NOT NULL,
    heiti VARCHAR(100) NOT NULL,

    CHECK(kennitala ~ '^[0-9]{10}$')
);

CREATE TABLE raforka_legacy.notendur_skraning (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    ar_stofnad integer NOT NULL,
    "X_HNIT" double precision,
    "Y_HNIT" double precision,
    eigandi_id integer,

    CHECK(ar_stofnad >= 1900 AND ar_stofnad <= EXTRACT(YEAR FROM CURRENT_DATE)),

    FOREIGN KEY(eigandi_id) REFERENCES raforka_legacy.fyrirtaeki_skraning(id)
    ON DELETE CASCADE
);


-- Task D1