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


USE `kantor`;
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

USE `kantor`;
CREATE  OR REPLACE VIEW `money_in_wallet` AS
SELECT
    w.wallet_id,
    w.user_id,
    COALESCE(SUM(t.value), 0) + COALESCE(SUM(it.value), 0) AS value_in_wallet
FROM
    wallet w
LEFT JOIN
    `transaction` t ON w.wallet_id = t.wallet_id
LEFT JOIN
    internal_transactions it ON w.wallet_id = it.wallet_id
GROUP BY
    w.wallet_id, w.user_id;


USE `kantor`;
DROP procedure IF EXISTS `user_registration`;

DELIMITER $$
USE `kantor`$$
CREATE PROCEDURE `user_registration`(u_password varchar(100), u_name varchar(45), u_surname varchar(45), u_email varchar(45))
BEGIN
INSERT INTO user (password_hash, name, surname, email)
VALUE (u_password, u_name, u_surname, u_email);
END$$

DELIMITER ;
