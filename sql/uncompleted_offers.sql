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