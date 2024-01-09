USE `kantor`;
DROP procedure IF EXISTS `user_registration`;

DELIMITER $$
USE `kantor`$$
CREATE PROCEDURE `user_registration`(u_password varchar(100), u_name varchar(45), u_surname varchar(45), u_email varchar(45))
BEGIN
INSERT INTO user (password, name, surname, email)
VALUE (u_password, u_name, u_surname, u_email);
END$$

DELIMITER ;