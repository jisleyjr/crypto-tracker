CREATE TABLE `position_sales` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Position_Id` int(11) NOT NULL,
  `Sale_Id` int(11) NOT NULL,
  `Qty` DECIMAL(65,9) NOT NULL,
   PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
