DELIMITER $$
USE `kantor`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_offer`(
    IN seller_id INT,
    IN publication_currency_id INT,
    IN cur_value DECIMAL(20, 2),
    IN wanted_curr_id INT,
    IN exchange_rate DECIMAL(20, 2)
)
BEGIN
    INSERT INTO offer_history (
        publication_date, 
        seller_id, 
        publication_currency_id, 
        value, 
        wanted_currency_id, 
        exchange_rate, 
        remaining_value, 
        is_cancelled
    )
    VALUES (
        NOW(), 
        seller_id, 
        publication_currency_id, 
        cur_value, 
        wanted_curr_id, 
        exchange_rate,
        cur_value, 
        false
    );
    SELECT LAST_INSERT_ID();
END$$

DELIMITER ;


DELIMITER $$
USE `kantor`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_internal_transaction`(u_id int, c_id int, cur_value decimal(20, 2))
BEGIN
DECLARE w_id INT;
SELECT wallet_id into w_id from wallet where user_id = u_id and currency_id = c_id;
	INSERT INTO internal_transactions (wallet_id, value)
    VALUES (w_id, cur_value);
END$$

DELIMITER ;


DELIMITER $$
USE `kantor`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `match_offers`(earlier_id int, later_id int, earlier_v decimal(20, 2), later_v decimal(20, 2))
BEGIN
DECLARE e_w_id INT;
DECLARE l_w_id INT;
DECLARE e_u_id INT;
DECLARE l_u_id INT;
DECLARE e_r_value decimal(20, 2);
DECLARE l_r_value decimal(20, 2);
DECLARE e_c_id INT;
DECLARE l_c_id INT;
SELECT seller_id, remaining_value, publication_currency_id INTO e_u_id, e_r_value, e_c_id from offer_history where offer_history_id = earlier_id;
SELECT seller_id, remaining_value, publication_currency_id INTO l_u_id, l_r_value, l_c_id from offer_history where offer_history_id = later_id;
SELECT wallet_id INTO e_w_id from wallet where user_id = e_u_id and currency_id = e_c_id;
SELECT wallet_id INTO l_w_id from wallet where user_id = l_u_id and currency_id = l_c_id;
INSERT INTO internal_transactions (wallet_id, value) VALUES (e_w_id, earlier_v);
INSERT INTO internal_transactions (wallet_id, value) VALUES (l_w_id, later_v);
update offer_history set remaining_value = e_r_value - earlier_v where offer_history_id = earlier_id;
update offer_history set remaining_value = l_r_value - later_v where offer_history_id = later_id;
INSERT INTO matched_offers (earlier_offer_id, later_offer_id, earlier_value, later_value) values (earlier_id, later_id, earlier_v, later_v);
END$$

DELIMITER ;