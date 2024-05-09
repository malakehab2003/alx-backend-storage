-- change the valid email to 0 if the email changed
DELIMITER $$
CREATE TRIGGER update_valid_email
BEFORE UPDATE ON users
FOR Each Row
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END $$
DELIMITER ;
