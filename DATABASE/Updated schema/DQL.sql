-- Task C5
/*Til að fá sendandi_maelingar notum við coalesce hérna, derived attribute. If stöð null then eining eigandi else stöð eigandi*/
SELECT
    m.*,
    COALESCE(s.eigandi, e.eigandi) AS sendandi_maelingar
FROM raforka_updated.orku_maelingar m
JOIN raforka_updated.orku_einingar e
    ON m.eining_id = e.id
LEFT JOIN raforka_updated.orku_einingar s
    ON m.stod = s.id;