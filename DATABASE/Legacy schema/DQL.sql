SELECT *
FROM raforka_legacy.notendur_skraning;

SELECT *
FROM raforka_legacy.notendur_skraning_id_seq;

SELECT * 
FROM raforka_legacy.orku_einingar;

SELECT *
FROM raforka_legacy.test_measurement;

SELECT * 
FROM raforka_legacy.orku_einingar_id_seq;

SELECT *
FROM raforka_legacy.orku_maelingar
LIMIT 100;

select *
from raforka_legacy.orku_maelingar
where tegund_maelingar ilike 'úttekt'
LIMIT 100;

-- Task A2

-- Querie 1
SELECT 
    eining_heiti as power_plant_source,
    EXTRACT(year FROM timi) as year,
    EXTRACT(month FROM timi) as month,
    tegund_maelingar as measurement_type,
    SUM(gildi_kwh) as total_kwh
FROM raforka_legacy.orku_maelingar
where EXTRACT(year FROM timi) = 2025
GROUP BY
    eining_heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    tegund_maelingar
ORDER BY power_plant_source, month, total_kwh DESC;


-- Querie 2
SELECT
    eining_heiti as power_plant_source,
    EXTRACT(YEAR FROM timi) as year,
    EXTRACT(MONTH FROM timi) as month,
    notandi_heiti as customer_name,
    sum(gildi_kwh) as total_kwh
FROM raforka_legacy.orku_maelingar
WHERE EXTRACT(year FROM timi) = 2025
AND notandi_heiti IS NOT NULL
GROUP BY
    eining_heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    notandi_heiti
ORDER BY power_plant_source, month, customer_name;


-- Querie 3
DROP VIEW IF EXISTS montly_power_plant_energy_view;

CREATE VIEW montly_power_plant_energy_view as
SELECT
    eining_heiti as power_plant_source,
    EXTRACT(YEAR FROM timi) as year,
    EXTRACT(MONTH FROM timi) as month,
    SUM(gildi_kwh) FILTER (WHERE tegund_maelingar = 'Framleiðsla') AS production_kwh,
    SUM(gildi_kwh) FILTER (WHERE tegund_maelingar = 'Innmötun') AS inflow_kwh,
    SUM(gildi_kwh) FILTER (WHERE tegund_maelingar = 'Úttekt') AS withdrawal_kwh
FROM raforka_legacy.orku_maelingar
WHERE EXTRACT(YEAR FROM timi) = 2025
GROUP BY
    eining_heiti,
    EXTRACT(YEAR FROM timi),
    EXTRACT(MONTH FROM timi);

SELECT
    power_plant_source,
    AVG((production_kwh - inflow_kwh) / production_kwh) AS plant_to_sub_loss_ratio,
    AVG((production_kwh - withdrawal_kwh) / production_kwh) AS total_system_loss_ratio
FROM montly_power_plant_energy_view
GROUP BY power_plant_source
ORDER BY power_plant_source ASC;

