USE `kantor`;
DROP function IF EXISTS `user_login`;

DELIMITER $$
USE `kantor`$$
CREATE FUNCTION `user_login` (u_login varchar(45), u_password varchar(45))
RETURNS bool
    READS SQL DATA
    DETERMINISTIC

BEGIN
declare u_id int;
SELECT user_id into u_id from user where login=u_login and password=u_password;
RETURN u_id;
END$$

DELIMITER ;