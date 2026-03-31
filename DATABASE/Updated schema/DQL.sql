-- Task C5


-- Show indexes in schema
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'raforka_updated';


-- Querie 1
DROP MATERIALIZED VIEW IF EXISTS raforka_updated.monthly_energy_flow_data_2025;
CREATE MATERIALIZED VIEW raforka_updated.monthly_energy_flow_data_2025 AS
SELECT
    oe.heiti as power_plant_source,
    EXTRACT(year FROM om.timi) as year,
    EXTRACT(month FROM om.timi) as month,
    om.tegund as measurement_type,
    SUM(om.gildi_kwh) as total_kwh
FROM raforka_updated.orku_maelingar om
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
WHERE timi >= DATE '2025-01-01'
    AND timi <  DATE '2026-01-01'
GROUP BY
    oe.heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    om.tegund
ORDER BY power_plant_source, month, total_kwh DESC;



-- Querie 2
DROP MATERIALIZED VIEW IF EXISTS raforka_updated.yearly_usage_by_company_2025;
CREATE MATERIALIZED VIEW raforka_updated.yearly_usage_by_company_2025 AS -- create materalized view must refresh manually to keep updated
SELECT
    oe.heiti as power_plant_source,
    EXTRACT(YEAR FROM timi) as year,
    EXTRACT(MONTH FROM timi) as month,
    en.heiti as customer_name,
    sum(om.gildi_kwh) as total_kwh
FROM raforka_updated.uttekt ut
JOIN raforka_updated.orku_maelingar om ON om.id = ut.maeling_id
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
JOIN raforka_updated.notendur_skraning ns ON ns.id = ut.notandi_id
JOIN raforka_updated.eigendur_notenda en ON en.id = ns.eigandi_id
WHERE timi >= DATE '2025-01-01'
    AND timi <  DATE '2026-01-01'
GROUP BY
    oe.heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    en.heiti
ORDER BY power_plant_source, month, customer_name;






--Querie 3
DROP MATERIALIZED VIEW IF EXISTS raforka_updated.montly_power_plant_energy_view_2025;
CREATE MATERIALIZED VIEW raforka_updated.montly_power_plant_energy_view_2025 as

SELECT
    oe.heiti as power_plant_source,
    EXTRACT(YEAR FROM om.timi) as year,
    EXTRACT(MONTH FROM om.timi) as month,
    SUM(gildi_kwh) FILTER (WHERE om.tegund = 'Framleiðsla') AS production_kwh,
    SUM(gildi_kwh) FILTER (WHERE om.tegund = 'Innmötun') AS inflow_kwh,
    SUM(gildi_kwh) FILTER (WHERE om.tegund = 'Úttekt') AS withdrawal_kwh
FROM raforka_updated.orku_maelingar om
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
WHERE timi >= DATE '2025-01-01'
    AND timi <  DATE '2026-01-01'
GROUP BY
    oe.heiti,
    EXTRACT(YEAR FROM om.timi),
    EXTRACT(MONTH FROM om.timi);

SELECT
    power_plant_source,
    AVG((production_kwh - inflow_kwh) / production_kwh) AS plant_to_sub_loss_ratio,
    AVG((production_kwh - withdrawal_kwh) / production_kwh) AS total_system_loss_ratio
FROM raforka_updated.montly_power_plant_energy_view_2025
GROUP BY power_plant_source
ORDER BY power_plant_source ASC;





--Custom queries

--For get_monthly_energy_flow_data, removing restriction on year 2025
DROP MATERIALIZED VIEW IF EXISTS raforka_updated.monthly_energy_flow_data;
CREATE MATERIALIZED VIEW raforka_updated.monthly_energy_flow_data AS
SELECT
    oe.heiti as power_plant_source,
    EXTRACT(year FROM om.timi) as year,
    EXTRACT(month FROM om.timi) as month,
    om.tegund as measurement_type,
    SUM(om.gildi_kwh) as total_kwh
FROM raforka_updated.orku_maelingar om
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
GROUP BY
    oe.heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    om.tegund
ORDER BY year, power_plant_source, month, total_kwh DESC;

--for get_monthly_company_usage_data
DROP MATERIALIZED VIEW IF EXISTS raforka_updated.yearly_usage_by_company;
CREATE MATERIALIZED VIEW raforka_updated.yearly_usage_by_company AS -- create materalized view must refresh manually to keep updated
SELECT
    oe.heiti as power_plant_source,
    EXTRACT(YEAR FROM timi) as year,
    EXTRACT(MONTH FROM timi) as month,
    en.heiti as customer_name,
    sum(om.gildi_kwh) as total_kwh
FROM raforka_updated.uttekt ut
JOIN raforka_updated.orku_maelingar om ON om.id = ut.maeling_id
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
JOIN raforka_updated.notendur_skraning ns ON ns.id = ut.notandi_id
JOIN raforka_updated.eigendur_notenda en ON en.id = ns.eigandi_id
GROUP BY
    oe.heiti,
    EXTRACT(year FROM timi),
    EXTRACT(month FROM timi),
    en.heiti
ORDER BY year, power_plant_source, month, customer_name;


--for get_monthly_plant_loss_ratios_data
DROP MATERIALIZED VIEW IF EXISTS raforka_updated.montly_power_plant_energy_view;
CREATE MATERIALIZED VIEW raforka_updated.montly_power_plant_energy_view as

SELECT
    oe.heiti as power_plant_source,
    EXTRACT(YEAR FROM om.timi) as year,
    EXTRACT(MONTH FROM om.timi) as month,
    SUM(gildi_kwh) FILTER (WHERE om.tegund = 'Framleiðsla') AS production_kwh,
    SUM(gildi_kwh) FILTER (WHERE om.tegund = 'Innmötun') AS inflow_kwh,
    SUM(gildi_kwh) FILTER (WHERE om.tegund = 'Úttekt') AS withdrawal_kwh
FROM raforka_updated.orku_maelingar om
JOIN raforka_updated.orku_einingar oe ON oe.id = om.eining_id
WHERE EXTRACT(YEAR FROM om.timi) = 2025
GROUP BY
    oe.heiti,
    EXTRACT(YEAR FROM om.timi),
    EXTRACT(MONTH FROM om.timi);
