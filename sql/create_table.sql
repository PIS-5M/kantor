CREATE DATABASE IF NOT EXISTS kantor;

CREATE TABLE `kantor`.`currency` (
  `currency_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `abbreviation` VARCHAR(5) NOT NULL,
  `account_number` VARCHAR(26) NOT NULL,
  PRIMARY KEY (`currency_id`));

CREATE TABLE `kantor`.`user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password_hash` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`));

CREATE TABLE `kantor`.`offer_history` (
  `offer_history_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `publication_date` DATETIME NOT NULL,
  `last_modification_date` DATETIME NULL,
  `seller_id` INT UNSIGNED NOT NULL,
  `publication_currency_id` INT UNSIGNED NOT NULL,
  `value` DECIMAL(20,2) NOT NULL,
  `wanted_currency_id` INT UNSIGNED NOT NULL,
  `exchange_rate` DECIMAL(20,2) NOT NULL,
  `account_number` VARCHAR(26) NOT NULL,
  PRIMARY KEY (`offer_history_id`),
  INDEX `seller_fk_idx` (`seller_id` ASC) VISIBLE,
  INDEX `publication_currency_fk_idx` (`publication_currency_id` ASC) VISIBLE,
  INDEX `wanted_currency_fk_idx` (`wanted_currency_id` ASC) VISIBLE,
  CONSTRAINT `seller_fk`
    FOREIGN KEY (`seller_id`)
    REFERENCES `kantor`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `publication_currency_fk`
    FOREIGN KEY (`publication_currency_id`)
    REFERENCES `kantor`.`currency` (`currency_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `wanted_currency_fk`
    FOREIGN KEY (`wanted_currency_id`)
    REFERENCES `kantor`.`currency` (`currency_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE `kantor`.`offer_history`
ADD COLUMN `remaining_value` DECIMAL(20,2) NOT NULL AFTER `account_number`;

CREATE TABLE `kantor`.`matched_offers` (
  `matched_offer_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `earlier_offer_id` INT UNSIGNED NOT NULL,
  `later_offer_id` INT UNSIGNED NOT NULL,
  `earlier_value` DECIMAL(20,2) NOT NULL,
  `later_value` DECIMAL(20,2) NOT NULL,
  PRIMARY KEY (`matched_offer_id`));

ALTER TABLE `kantor`.`matched_offers`
ADD INDEX `earlier_offer_idx` (`earlier_offer_id` ASC) VISIBLE,
ADD INDEX `later_offer_fk_idx` (`later_offer_id` ASC) VISIBLE;
;
ALTER TABLE `kantor`.`matched_offers`
ADD CONSTRAINT `earlier_offer_fk`
  FOREIGN KEY (`earlier_offer_id`)
  REFERENCES `kantor`.`offer_history` (`offer_history_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `later_offer_fk`
  FOREIGN KEY (`later_offer_id`)
  REFERENCES `kantor`.`offer_history` (`offer_history_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

CREATE TABLE `kantor`.`transaction` (
  `transaction_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `offer_id` INT UNSIGNED NOT NULL,
  `client_account_number` VARCHAR(26) NOT NULL,
  `value` DECIMAL(20,2) NOT NULL,
  `currency_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`transaction_id`));

  ALTER TABLE `kantor`.`transaction`
ADD INDEX `offer_fk_idx` (`offer_id` ASC) VISIBLE,
ADD INDEX `currency_fk_idx` (`currency_id` ASC) VISIBLE;
;
ALTER TABLE `kantor`.`transaction`
ADD CONSTRAINT `offer_fk`
  FOREIGN KEY (`offer_id`)
  REFERENCES `kantor`.`offer_history` (`offer_history_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `currency_fk`
  FOREIGN KEY (`currency_id`)
  REFERENCES `kantor`.`currency` (`currency_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;
