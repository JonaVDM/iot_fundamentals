-- Create the climate table
CREATE TABLE `climate`.`climate` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `device_id` TEXT NOT NULL,
  `uploaded` BOOLEAN NOT NULL,
  `time` TIMESTAMP NOT NULL,
  `temperature` FLOAT NOT NULL,
  `pressure` FLOAT NOT NULL,
  `humidity` FLOAT NOT NULL,

  PRIMARY KEY (`id`),
  INDEX (`device_id`)
) ENGINE = InnoDB; 
