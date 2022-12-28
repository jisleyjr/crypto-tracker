INSERT INTO `crypto-tracker`.`sales`
(
`Order_Id`,
`Order_Date`,
`Coin`,
`Qty`,
`Price`,
`Total_Proceeds`
)
(
SELECT Order_Id, Max(Time) as Order_Date,  
Base_Asset as Coin, SUM(Realized_Amount_For_Base_Asset) as Qty,
SUM(Realized_Amount_For_Base_Asset_In_USD_Value) / SUM(Realized_Amount_For_Base_Asset) as Price, 
SUM(Realized_Amount_For_Base_Asset_In_USD_Value) as Total_Proceeds
FROM transactions
WHERE Category = 'Spot Trading' and Base_Asset = 'Flux' and Quote_Asset = 'USD' and Operation = 'Sell'
GROUP BY Order_Id
ORDER BY Base_Asset asc, Order_Date asc
);
