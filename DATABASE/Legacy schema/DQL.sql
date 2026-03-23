SELECT *
FROM raforka_legacy.notendur_skraning

SELECT *
FROM raforka_legacy.notendur_skraning_id_seq

SELECT * 
FROM raforka_legacy.orku_einingar


SELECT * 
FROM raforka_legacy.orku_einingar_id_seq

SELECT *
FROM raforka_legacy.orku_maelingar
LIMIT 20

-- Task A2

-- Querie 1
-- Calculate the sum of kwh for each month and each type in 2025
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
-- Calculate the sum of kwh for each customer every month in 2025
SELECT
    eining_heiti as power_plant_source,
    EXTRACT(year FROM timi) as year, 
    EXTRACT(month FROM timi) as month,
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
