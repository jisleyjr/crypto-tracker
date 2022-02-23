LOAD DATA INFILE 'binanceus_2020.csv'
INTO TABLE transations
FIELDS TERMINATED BY ','
IGNORE 1 ROWS
(User_Id,Time,Category,Operation,Order_Id,Transaction_Id,
Primary_Asset,@Realized_Amount_For_Primary_Asset,@Realized_Amount_For_Primary_Asset_In_USD_Value,
Base_Asset,@Realized_Amount_For_Base_Asset,@Realized_Amount_For_Base_Asset_In_USD_Value,
Quote_Asset,@Realized_Amount_For_Quote_Asset,@Realized_Amount_For_Quote_Asset_In_USD_Value,
Fee_Asset,@Realized_Amount_For_Fee_Asset,@Realized_Amount_For_Fee_Asset_In_USD_Value,
Payment_Method,Withdrawal_Method,Additional_Note)
SET Realized_Amount_For_Primary_Asset = IF(STRCMP(@Realized_Amount_For_Primary_Asset, ''), null, CONVERT(@Realized_Amount_For_Primary_Asset, DECIMAL)),
Realized_Amount_For_Primary_Asset_In_USD_Value = IF(STRCMP(@Realized_Amount_For_Primary_Asset, ''), null, CONVERT(@Realized_Amount_For_Primary_Asset_In_USD_Value, DECIMAL)),
Realized_Amount_For_Base_Asset = IF(STRCMP(@Realized_Amount_For_Base_Asset, ''), null, CONVERT(@Realized_Amount_For_Base_Asset, DECIMAL)),
Realized_Amount_For_Base_Asset_In_USD_Value = IF(STRCMP(@Realized_Amount_For_Base_Asset_In_USD_Value, ''), null, CONVERT(@Realized_Amount_For_Base_Asset_In_USD_Value, DECIMAL)),
Realized_Amount_For_Quote_Asset = IF(STRCMP(@Realized_Amount_For_Quote_Asset, ''), null, CONVERT(@Realized_Amount_For_Quote_Asset, DECIMAL)),
Realized_Amount_For_Quote_Asset_In_USD_Value = IF(STRCMP(@Realized_Amount_For_Quote_Asset_In_USD_Value, ''), null, CONVERT(@Realized_Amount_For_Quote_Asset_In_USD_Value, DECIMAL)),
Realized_Amount_For_Fee_Asset = IF(STRCMP(@Realized_Amount_For_Fee_Asset, ''), null, CONVERT(@Realized_Amount_For_Fee_Asset, DECIMAL)),
Realized_Amount_For_Fee_Asset_In_USD_Value = IF(STRCMP(@Realized_Amount_For_Fee_Asset_In_USD_Value, ''), null, CONVERT(@Realized_Amount_For_Fee_Asset_In_USD_Value, DECIMAL))
;