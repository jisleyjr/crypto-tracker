CREATE TABLE `sales` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Order_Id` varchar(50) DEFAULT NULL,
  `Order_Date` timestamp,
  `Coin` varchar(50) DEFAULT NULL,
  `Qty` DECIMAL(65,9) DEFAULT NULL,
  `Price` DECIMAL(65,6) DEFAULT NULL,
  `Total_Proceeds` DECIMAL(65,6) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
