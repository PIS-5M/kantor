CREATE DATABASE IF NOT EXISTS kantor;

CREATE TABLE `user` (
  `user_id` int unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `surname` varchar(45) NOT NULL,
  `bank_account_hash` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `phone_number` varchar(12) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `Login_UNIQUE` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `currency` (
  `currency_id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`currency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `country` (
  `country_id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `currency_id` int unsigned NOT NULL,
  PRIMARY KEY (`country_id`),
  KEY `country_corrency_fk_idx` (`currency_id`),
  CONSTRAINT `country_corrency_fk` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`currency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `exchange_rate` (
  `exchange_rate_id` int unsigned NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `value` decimal(11,4) NOT NULL,
  `currency_id` int unsigned NOT NULL,
  PRIMARY KEY (`exchange_rate_id`),
  KEY `exchange_rate_currency_idx` (`currency_id`),
  CONSTRAINT `exchange_rate_currency` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`currency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `favourite_currency` (
  `favourite_currency_id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int unsigned NOT NULL,
  `currency_id` int unsigned NOT NULL,
  PRIMARY KEY (`favourite_currency_id`),
  KEY `favourite_currency_user_fk_idx` (`user_id`),
  KEY `favourite_currency_currency_fk_idx` (`currency_id`),
  CONSTRAINT `favourite_currency_currency_fk` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`currency_id`),
  CONSTRAINT `favourite_currency_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `transaction_history` (
  `transaction_history_id` int unsigned NOT NULL AUTO_INCREMENT,
  `value` decimal(20,2) NOT NULL,
  `value_currency_id` int unsigned NOT NULL,
  `price` decimal(20,2) NOT NULL,
  `price_currency_id` int unsigned NOT NULL,
  `publication_date` datetime NOT NULL,
  `seller_id` int unsigned NOT NULL,
  `reservation_date` datetime DEFAULT NULL,
  `buyer_id` int unsigned DEFAULT NULL,
  `payment_date_seller` datetime DEFAULT NULL,
  `payment_date_buyer` datetime DEFAULT NULL,
  `commission` decimal(20,2) DEFAULT NULL,
  PRIMARY KEY (`transaction_history_id`),
  KEY `transaction_history_value_currency_fk_idx` (`value_currency_id`),
  KEY `transaction_history_price_currency_fk_idx` (`price_currency_id`),
  KEY `transaction_history__idx` (`seller_id`),
  KEY `transaction_history_buyer_fk_idx` (`buyer_id`),
  CONSTRAINT `transaction_history_buyer_fk` FOREIGN KEY (`buyer_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `transaction_history_price_currency_fk` FOREIGN KEY (`price_currency_id`) REFERENCES `currency` (`currency_id`),
  CONSTRAINT `transaction_history_seller_fk` FOREIGN KEY (`seller_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `transaction_history_value_currency_fk` FOREIGN KEY (`value_currency_id`) REFERENCES `currency` (`currency_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

