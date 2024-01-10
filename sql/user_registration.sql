USE `kantor`;
DROP procedure IF EXISTS `user_registration`;

DELIMITER $$
USE `kantor`$$
CREATE PROCEDURE `user_registration`(u_password varchar(100), u_name varchar(45), u_surname varchar(45), u_email varchar(100))
BEGIN
INSERT INTO user (name, surname, email, password_hash)
VALUE (u_name, u_surname, u_email, u_password);
END$$

DELIMITER ;
