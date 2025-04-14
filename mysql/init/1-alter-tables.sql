USE `crypto-tracker`;
ALTER TABLE `crypto-tracker`.`transactions` 
CHANGE COLUMN `User_Id` `User_Id` VARCHAR(50) NULL DEFAULT NULL ;
ADD COLUMN `Source` VARCHAR(50) NULL DEFAULT 'coinbase' AFTER `User_Id`,

ALTER TABLE `crypto-tracker`.`sales` 
ADD COLUMN `Source` VARCHAR(45) NULL DEFAULT 'binanceus' AFTER `Processed`;

ALTER TABLE `crypto-tracker`.`positions` 
ADD COLUMN `Source` VARCHAR(45) NULL DEFAULT 'binanceus' AFTER `Total_Cost`;
