-- Task A2
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

SELECT eining_heiti, EXTRACT(year FROM timi) as year, EXTRACT(month FROM timi) as month, tegund_maelingar, SUM(gildi_kwh) as total_kwh
FROM raforka_legacy.orku_maelingar
where EXTRACT(year FROM timi) = 2025
GROUP BY eining_heiti, EXTRACT(year FROM timi), EXTRACT(month FROM timi), tegund_maelingar, total_kwh
LIMIT 50