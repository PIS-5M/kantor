CREATE DATABASE IF NOT EXISTS kantor;

CREATE TABLE `kantor`.`currency` (
  `currency_id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `abbreviation` varchar(5) NOT NULL,
  `account_number` varchar(26) NOT NULL,
  PRIMARY KEY (`currency_id`)
);

CREATE TABLE `kantor`.`user` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `surname` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
);

CREATE TABLE `kantor`.`wallet` (
  `wallet_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `currency_id` int unsigned NOT NULL,
  `account_number_hash` varchar(100) NOT NULL,
  PRIMARY KEY (`wallet_id`),
  KEY `user_wallet_idx` (`user_id`),
  KEY `currency_wallet_fk_idx` (`currency_id`),
  CONSTRAINT `currency_wallet_fk` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`currency_id`),
  CONSTRAINT `user_wallet_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `kantor`.`offer_history` (
  `offer_history_id` int unsigned NOT NULL AUTO_INCREMENT,
  `publication_date` datetime NOT NULL,
  `last_modification_date` datetime DEFAULT NULL,
  `seller_id` int unsigned NOT NULL,
  `publication_currency_id` int unsigned NOT NULL,
  `value` decimal(20,2) NOT NULL,
  `wanted_currency_id` int unsigned NOT NULL,
  `exchange_rate` decimal(20,2) NOT NULL,
  `remaining_value` decimal(20,2) NOT NULL,
  `is_cancelled` bit(1) NOT NULL,
  PRIMARY KEY (`offer_history_id`),
  KEY `seller_fk_idx` (`seller_id`),
  KEY `publication_currency_fk_idx` (`publication_currency_id`),
  KEY `wanted_currency_fk_idx` (`wanted_currency_id`),
  CONSTRAINT `publication_currency_fk` FOREIGN KEY (`publication_currency_id`) REFERENCES `currency` (`currency_id`),
  CONSTRAINT `seller_fk` FOREIGN KEY (`seller_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `wanted_currency_fk` FOREIGN KEY (`wanted_currency_id`) REFERENCES `currency` (`currency_id`)
);

CREATE TABLE `kantor`.`matched_offers` (
  `matched_offer_id` int unsigned NOT NULL AUTO_INCREMENT,
  `earlier_offer_id` int unsigned NOT NULL,
  `later_offer_id` int unsigned NOT NULL,
  `earlier_value` decimal(20,2) NOT NULL,
  `later_value` decimal(20,2) NOT NULL,
  PRIMARY KEY (`matched_offer_id`),
  KEY `earlier_offer_idx` (`earlier_offer_id`),
  KEY `later_offer_fk_idx` (`later_offer_id`),
  CONSTRAINT `earlier_offer_fk` FOREIGN KEY (`earlier_offer_id`) REFERENCES `offer_history` (`offer_history_id`),
  CONSTRAINT `later_offer_fk` FOREIGN KEY (`later_offer_id`) REFERENCES `offer_history` (`offer_history_id`)
);

CREATE TABLE `kantor`.`transaction` (
  `transaction_id` int unsigned NOT NULL AUTO_INCREMENT,
  `wallet_id` int unsigned NOT NULL,
  `value` decimal(20,2) NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `wallet_transaction_idx` (`wallet_id`),
  CONSTRAINT `wallet_transaction` FOREIGN KEY (`wallet_id`) REFERENCES `wallet` (`wallet_id`)
);

CREATE TABLE `kantor`.`internal_transactions` (
  `internal_transactions_id` int NOT NULL AUTO_INCREMENT,
  `wallet_id` int unsigned NOT NULL,
  `value` decimal(20,2) NOT NULL,
  PRIMARY KEY (`internal_transactions_id`),
  KEY `insternal_transaction_fk_idx` (`wallet_id`),
  CONSTRAINT `insternal_transaction_fk` FOREIGN KEY (`wallet_id`) REFERENCES `wallet` (`wallet_id`)
);

USE kantor;
CREATE OR REPLACE VIEW `money_on_offer` AS
SELECT
    w.wallet_id,
    w.user_id,
    c.name AS currency_name,
    COALESCE(SUM(CASE WHEN oh.is_cancelled = 0 THEN oh.remaining_value ELSE 0 END), 0) AS value_in_offer
FROM
    wallet w
LEFT JOIN
    offer_history oh ON w.user_id = oh.seller_id AND w.currency_id = oh.publication_currency_id AND oh.is_cancelled = 0
LEFT JOIN
    currency c ON w.currency_id = c.currency_id
GROUP BY
    w.wallet_id;

USE kantor;
CREATE  OR REPLACE VIEW money_in_wallet AS
SELECT w.wallet_id, w.user_id, COALESCE(SUM(total_value), 0) as value_in_wallet
FROM wallet w
LEFT JOIN (
    SELECT wallet_id, SUM(value) as total_value
    FROM internal_transactions
    GROUP BY wallet_id
    
    UNION ALL
    
    SELECT wallet_id, SUM(value) as total_value
    FROM transaction
    GROUP BY wallet_id
) AS combined_results
ON w.wallet_id = combined_results.wallet_id
GROUP BY w.wallet_id;

INSERT INTO `kantor`.`currency` (`currency_id`, `name`, `abbreviation`, `account_number`) VALUES
(1, 'Dolar Amerykański', 'USD', '12345678901234567890123456'),
(2, 'Euro', 'EUR', '98765432109876543210987654');

INSERT INTO `kantor`.`user` (`user_id`, `name`, `surname`, `email`, `password_hash`) VALUES
(1, 'Bot', 'Jeden', 'bot1@example.com', 'hash1'),
(2, 'Bot', 'Dwa', 'bot2@example.com', 'hash2'),
(3, 'Bot', 'Trzy', 'bot3@example.com', 'hash3');

INSERT INTO `kantor`.`wallet` (`wallet_id`, `user_id`, `currency_id`, `account_number_hash`) VALUES
(1, 1, 1, 'aaaaa1'),
(2, 1, 2, 'aaaaa2'),
(3, 2, 1, 'aaaaa3'),
(4, 2, 2, 'aaaaa4'),
(5, 3, 1, 'aaaaa5'),
(6, 3, 2, 'aaaaa6');

INSERT INTO `kantor`.`transaction` (`transaction_id`, `wallet_id`, `value`) VALUES
(1, 1, 1000),
(2, 2, 1000),
(3, 3, 1000),
(4, 4, 1000),
(5, 5, 1000),
(6, 6, 1000);

USE `kantor`;
CREATE
     OR REPLACE ALGORITHM = UNDEFINED
    DEFINER = `root`@`localhost`
    SQL SECURITY DEFINER
VIEW `uncompleted_offers` AS
    SELECT
        `offer_history`.`offer_history_id` AS `offer_history_id`,
        `offer_history`.`publication_date` AS `publication_date`,
        `offer_history`.`last_modification_date` AS `last_modification_date`,
        `offer_history`.`seller_id` AS `seller_id`,
        `offer_history`.`publication_currency_id` AS `publication_currency_id`,
        `offer_history`.`value` AS `value`,
        `offer_history`.`wanted_currency_id` AS `wanted_currency_id`,
        `offer_history`.`exchange_rate` AS `exchange_rate`,
        `offer_history`.`remaining_value` AS `remaining_value`,
        `offer_history`.`is_cancelled` AS `is_cancelled`
    FROM
        `offer_history`

    WHERE
        ((`offer_history`.`remaining_value` > 0)
            AND ((0 <> `offer_history`.`is_cancelled`)
            IS FALSE));

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
SELECT wallet_id INTO e_w_id from wallet where user_id = e_u_id and currency_id = l_c_id;
SELECT wallet_id INTO l_w_id from wallet where user_id = l_u_id and currency_id = e_c_id;
INSERT INTO internal_transactions (wallet_id, value) VALUES (e_w_id, later_v);
INSERT INTO internal_transactions (wallet_id, value) VALUES (l_w_id, earlier_v);
update offer_history set remaining_value = e_r_value - earlier_v where offer_history_id = earlier_id;
update offer_history set remaining_value = l_r_value - later_v where offer_history_id = later_id;
INSERT INTO matched_offers (earlier_offer_id, later_offer_id, earlier_value, later_value) values (earlier_id, later_id, earlier_v, later_v);
END$$

DELIMITER ;