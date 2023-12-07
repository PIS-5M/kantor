USE `kantor`;
DROP procedure IF EXISTS `user_registration`;

DELIMITER $$
USE `kantor`$$
CREATE PROCEDURE `user_registration`(u_login varchar(45), u_password varchar(45), 
								u_name varchar(45), u_surname varchar(45), 
                                u_bank_account_hash varchar(45), u_email varchar(45), u_phone_number varchar(45))
BEGIN
INSERT INTO user (login, password, name, surname, bank_account_hash, email, phone_number) 
VALUE (u_login, u_password, u_name, u_surname, u_bank_account_hash, u_email, u_phone_number); 
END$$

DELIMITER ;