INSERT INTO `crypto-tracker`.`positions`
(
`Order_Id`,
`Order_Date`,
`Coin`,
`Original_Qty`,
`Remaining_Qty`,
`Price`)
(
SELECT Order_Id, Time as Order_Date,  
Base_Asset as Coin, SUM(Realized_Amount_For_Base_Asset) as Qty, SUM(Realized_Amount_For_Base_Asset) as Qty, 
Realized_Amount_For_Base_Asset_In_USD_Value / Realized_Amount_For_Base_Asset as Price
FROM transactions
WHERE Category = 'Spot Trading' and Base_Asset = 'Flux' and Quote_Asset = 'USD' and Operation = 'Buy'
GROUP BY Order_Id
ORDER BY Base_Asset asc, Time asc
);
