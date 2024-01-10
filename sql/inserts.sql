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