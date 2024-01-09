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
  `client_account_number` varchar(26) NOT NULL,
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




