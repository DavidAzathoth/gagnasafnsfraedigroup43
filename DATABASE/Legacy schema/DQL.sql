SELECT *
FROM raforka_legacy.notendur_skraning;

SELECT *
FROM raforka_legacy.notendur_skraning_id_seq;

SELECT * 
FROM raforka_legacy.orku_einingar;


SELECT * 
FROM raforka_legacy.orku_einingar_id_seq;

SELECT *
FROM raforka_legacy.orku_maelingar
LIMIT 20;

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
ORDER BY eining_heiti, month, total_kwh DESC;


-- Querie 2


