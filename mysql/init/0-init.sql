USE `crypto-tracker`;

CREATE TABLE `transactions` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `User_Id` int(11) DEFAULT NULL,
  `Time` timestamp,
  `Category` varchar(50) DEFAULT NULL,
  `Operation` varchar(50) DEFAULT NULL,
  `Order_Id` varchar(50) DEFAULT NULL,
  `Transaction_Id` varchar(50) DEFAULT NULL,
  `Primary_Asset` varchar(50) DEFAULT NULL,
  `Realized_Amount_For_Primary_Asset` DECIMAL(65,9) DEFAULT NULL,
  `Realized_Amount_For_Primary_Asset_In_USD_Value` DECIMAL(65,6) DEFAULT NULL,
  `Base_Asset` varchar(50) DEFAULT NULL,
  `Realized_Amount_For_Base_Asset` DECIMAL(65,9) DEFAULT NULL,
  `Realized_Amount_For_Base_Asset_In_USD_Value` DECIMAL(65,6) DEFAULT NULL,
  `Quote_Asset` varchar(50) DEFAULT NULL,
  `Realized_Amount_For_Quote_Asset` DECIMAL(65,9) DEFAULT NULL,
  `Realized_Amount_For_Quote_Asset_In_USD_Value` DECIMAL(65,6) DEFAULT NULL,
  `Fee_Asset` varchar(50) DEFAULT NULL,
  `Realized_Amount_For_Fee_Asset` DECIMAL(65,9) DEFAULT NULL,
  `Realized_Amount_For_Fee_Asset_In_USD_Value` DECIMAL(65,6) DEFAULT NULL,
  `Payment_Method` varchar(50) DEFAULT NULL,
  `Withdrawal_Method` varchar(50) DEFAULT NULL,
  `Additional_Note` varchar(50) DEFAULT NULL,
  `Processed` bit DEFAULT 0,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `positions` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Order_Id` varchar(50) DEFAULT NULL,
  `Order_Date` timestamp DEFAULT NULL,
  `Coin` varchar(50) DEFAULT NULL,
  `Original_Qty` DECIMAL(65,9) DEFAULT NULL,
  `Remaining_Qty` DECIMAL(65,9) DEFAULT NULL,
  `Price` DECIMAL(65,6) DEFAULT NULL,
  `Total_Cost` DECIMAL(65,6) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `sales` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Order_Id` varchar(50) DEFAULT NULL,
  `Order_Date` timestamp DEFAULT NULL,
  `Coin` varchar(50) DEFAULT NULL,
  `Qty` DECIMAL(65,9) DEFAULT NULL,
  `Price` DECIMAL(65,6) DEFAULT NULL,
  `Total_Proceeds` DECIMAL(65,6) DEFAULT NULL,
  `Processed` bit DEFAULT 0,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*
TODO : Add indexes and foreign key
*/
CREATE TABLE `position_sales` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Position_Id` int(11) NOT NULL,
  `Sale_Id` int(11) NOT NULL,
  `Qty` DECIMAL(65,9) NOT NULL,
   PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

