CREATE DATABASE IF NOT EXISTS python_assignment;
USE python_assignment;


CREATE TABLE IF NOT EXISTS  `financial_data`  (
  `id` INT(0) NOT NULL AUTO_INCREMENT,
  `symbol` VARCHAR(40) NOT NULL,
  `date` DATE NOT NULL,
  `open_price` FLOAT NOT NULL,
  `close_price` FLOAT NOT NULL,
  `volume` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB CHARACTER SET=utf8;