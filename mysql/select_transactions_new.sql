SELECT Id, Time, Category, Operation, Order_Id, Transaction_Id, 
Base_Asset, Realized_Amount_For_Base_Asset, Realized_Amount_For_Base_Asset_In_USD_Value, Realized_Amount_For_Base_Asset_In_USD_Value / Realized_Amount_For_Base_Asset as Base_Asset_Price,
Quote_Asset, Realized_Amount_For_Quote_Asset, Realized_Amount_For_Quote_Asset_In_USD_Value, Processed
FROM cracker.transations_new
WHERE Category = 'Spot Trading' and Base_Asset = 'BCH'
ORDER BY Base_Asset asc, Time asc