CREATE TABLE `positions` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Order_Id` varchar(50) DEFAULT NULL,
  `Order_Date` timestamp,
  `Coin` varchar(50) DEFAULT NULL,
  `Original_Qty` DECIMAL(65,9) DEFAULT NULL,
  `Remaining_Qty` DECIMAL(65,9) DEFAULT NULL,
  `Price` DECIMAL(65,6) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*
 User_Id,Time,Category,Operation,Order_Id,Transaction_Id,Primary_Asset,Realized_Amount_For_Primary_Asset,Realized_Amount_For_Primary_Asset_In_USD_Value,Base_Asset,Realized_Amount_For_Base_Asset,Realized_Amount_For_Base_Asset_In_USD_Value,Quote_Asset,Realized_Amount_For_Quote_Asset,Realized_Amount_For_Quote_Asset_In_USD_Value,Fee_Asset,Realized_Amount_For_Fee_Asset,Realized_Amount_For_Fee_Asset_In_USD_Value,Payment_Method,Withdrawal_Method,Additional_Note*/
