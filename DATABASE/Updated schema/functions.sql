CREATE OR REPLACE FUNCTION set_sendandi()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stod IS NULL THEN
        SELECT eigandi INTO NEW.sendandi_maelingar
        FROM raforka_updated.orku_einingar
        WHERE id = NEW.eining_id;
    ELSE
        SELECT eigandi INTO NEW.sendandi_maelingar
        FROM raforka_updated.orku_einingar
        WHERE id = NEW.stod;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;