-- Task C3


DROP TABLE IF EXISTS
    raforka_updated.eigendur_notenda,
    raforka_updated.eigendur_eininga,
    raforka_updated.notendur_skraning,
    raforka_updated.orku_einingar,
    raforka_updated.stodvar,
    raforka_updated.virkjanir,
    raforka_updated.orku_maelingar,
    raforka_updated.uttekt,
    raforka_updated.framleidsla,
    raforka_updated.innmotun
    CASCADE

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

CREATE TABLE raforka_updated.eigendur_eininga(
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL
);

CREATE TABLE raforka_updated.notendur_skraning (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    ar_stofnad int NOT NULL,
    "X_HNIT" decimal(9, 6) NOT NULL,
    "Y_HNIT" decimal(9, 6) NOT NULL,
    eigandi_id int REFERENCES raforka_updated.eigendur_notenda(id),

    CHECK(ar_stofnad >= 1900 AND ar_stofnad <= EXTRACT(YEAR FROM CURRENT_DATE))
);


CREATE TABLE raforka_updated.orku_einingar (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    heiti VARCHAR(100) NOT NULL,
    tegund VARCHAR(100),
    eigandi_id int REFERENCES raforka_updated.eigendur_eininga(id),
    ar_uppsett date NOT NULL,
    "X_HNIT" decimal(9, 6) NOT NULL,
    "Y_HNIT" decimal(9, 6) NOT NULL,
    tengd_stod int REFERENCES raforka_updated.orku_einingar(id),
    CHECK (tengd_stod <> id)
);

--------------------------
--delete?
--------------------------

-- CREATE TABLE raforka_updated.stodvar (
--     id int PRIMARY KEY REFERENCES raforka_updated.orku_einingar(id),
--     tegund_stod VARCHAR(50) DEFAULT 'Aðveitustöð'
-- );

-- CREATE TABLE raforka_updated.virkjanir (
--     id int PRIMARY KEY REFERENCES raforka_updated.orku_einingar(id),
--     tegund_stod VARCHAR(50)
-- );


CREATE TABLE raforka_updated.orku_maelingar (
    id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    eining_id int NOT NULL REFERENCES raforka_updated.orku_einingar(id),
    tegund VARCHAR(11) CHECK (
        LOWER(tegund) IN ('framleiðsla', 'innmötun', 'úttekt')),
    timi timestamp without time zone,
    gildi_kwh numeric
);


CREATE TABLE raforka_updated.uttekt (
    maeling_id int PRIMARY KEY 
        REFERENCES raforka_updated.orku_maelingar(id),
    notandi_id int NOT NULL 
        REFERENCES raforka_updated.notendur_skraning(id)
);

select om.id, om.eining_id, om.tegund, om.timi, om.gildi_kwh
from raforka_updated.orku_maelingar om
where om.tegund = 'Úttekt'
limit 10;

EXPLAIN ANALYZE
select *
from raforka_legacy.orku_maelingar
where tegund_maelingar = 'Úttekt'
limit 100000;

CREATE INDEX ON raforka_updated.orku_maelingar(eining_id)
CREATE INDEX ON raforka_updated.notendur_skraning(eigandi_id)
CREATE INDEX ON raforka_updated.orku_einingar(eigandi_id)

CREATE INDEX ON raforka_updated.uttekt(maeling_id)
CREATE INDEX ON raforka_updated.uttekt(notandi_id)
EXPLAIN ANALYZE
select om.id, oe.heiti, om.tegund, CASE
WHEN om.tegund = 'Framleiðsla' THEN ee.heiti
WHEN om.tegund = 'Innmötun' THEN (
    oe1.heiti
)
ELSE (
    SELECT oe2.heiti
    FROM raforka_updated.orku_einingar oe2
    WHERE oe2.heiti = 'S3_Vestmannaeyjar'
)
END as "sendandi_maelingar", om.timi, om.gildi_kwh, en.heiti as notandi
from raforka_updated.uttekt ut
JOIN raforka_updated.orku_maelingar om ON om.id = ut.maeling_id
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
JOIN raforka_updated.notendur_skraning ns ON ns.id = ut.notandi_id
JOIN raforka_updated.eigendur_notenda en ON en.id = ns.eigandi_id
JOIN raforka_updated.eigendur_eininga ee ON ee.id = oe.eigandi_id
JOIN raforka_updated.orku_einingar oe1 ON oe1.id = oe.tengd_stod
limit 1000
----------------
--delete?
----------------

-- CREATE TABLE raforka_updated.framleidsla (
--     maeling_id int PRIMARY KEY 
--         REFERENCES raforka_updated.orku_maelingar(id),
--     virkjun_id int NOT NULL 
--         REFERENCES raforka_updated.virkjanir(id)
-- );

-- CREATE TABLE raforka_updated.innmotun (
--     maeling_id int PRIMARY KEY 
--         REFERENCES raforka_updated.orku_maelingar(id),
--     stod_id int NOT NULL
--         REFERENCES raforka_updated.stodvar(id)
-- );


----------------------------------------------------------------
    --1
    CREATE TEMP TABLE id_map (
        old_id INT,
        new_id INT
    );


    --2
    INSERT INTO raforka_updated.orku_einingar
    (heiti, tegund, eigandi_id, ar_uppsett, "X_HNIT", "Y_HNIT")
    SELECT
        heiti,
        tegund,
        eigandi_id,
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

EXPLAIN ANALYZE
select om.id, oe.heiti, om.tegund, 
CASE
WHEN om.tegund = 'Framleiðsla' THEN ee.heiti
WHEN om.tegund = 'Innmötun' THEN (
    oe1.heiti
)
ELSE (
    SELECT oe2.heiti
    FROM raforka_updated.orku_einingar oe2
    WHERE oe2.heiti = 'S3_Vestmannaeyjar'
)
END as "sendandi_maelingar",
om.timi, om.gildi_kwh
from raforka_updated.orku_maelingar om
join raforka_updated.orku_einingar oe ON oe.id = om.eining_id
JOIN raforka_updated.eigendur_eininga ee ON ee.id = oe.eigandi_id
JOIN raforka_updated.orku_einingar oe1 ON oe1.id = oe.id
ORDER BY om.id
limit 1000


select *
from raforka_updated.orku_maelingar
limit 100


select *
from raforka_legacy.orku_maelingar
limit 1000
where id = 1

EXPLAIN ANALYZE
select *
from raforka_legacy.orku_einingar;

select * 
from raforka_legacy.orku_maelingar
LIMIT 1000;

select * 
from raforka_updated.orku_einingar;


select *
from raforka_updated.stodvar;

select *
from raforka_updated.virkjanir;

select *
from raforka_legacy.orku_maelingar om
where om.tegund_maelingar = 'Úttekt'
ORDER BY om.id
limit 10;

SELECT om.id, oldoe.eining_heiti, oldoe.id, oldoe.notandi_heiti, om.gildi_kwh
FROM raforka_updated.orku_maelingar om
JOIN raforka_legacy.orku_maelingar oldoe
ON oldoe.timi = om.timi
AND oldoe.gildi_kwh = om.gildi_kwh
WHERE om.tegund = 'Úttekt'
ORDER BY om.id
limit 10


EXPLAIN ANALYZE
SELECT 
    om.id,
    oe.heiti,
    om.tegund,

    CASE
        WHEN om.tegund = 'Framleiðsla' THEN ee.heiti
        WHEN om.tegund = 'Innmötun' THEN ee_s.heiti
        ELSE 'S3_Vestmannaeyjar'
    END AS sendandi_maelingar,

    om.timi,
    om.gildi_kwh

select *
from raforka_updated.orku_einingar
FROM raforka_updated.orku_maelingar om

select *
from raforka_updated.orku_maelingar
where old_id = 302;

select *
from raforka_legacy.orku_maelingar
where id = 302;
SELECT COUNT(*) 
FROM raforka_updated.orku_maelingar;

SELECT COUNT(*)
from raforka_legacy.orku_maelingar;
JOIN raforka_updated.orku_einingar oe 
    ON oe.id = om.eining_id

JOIN raforka_updated.eigendur_eininga ee 
    ON ee.id = oe.eigandi_id

LEFT JOIN raforka_updated.orku_einingar oe_s
    ON oe.tengd_stod = oe_s.id

LEFT JOIN raforka_updated.eigendur_eininga ee_s
    ON ee_s.id = oe_s.eigandi_id

LIMIT 100000;
-- Task D1