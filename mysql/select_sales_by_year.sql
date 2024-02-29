SELECT sales.Coin, sales.Order_id, sales.Order_Date as Sales_Date, 
positions.Order_Date as Buy_Date,
ps.Qty * sales.Price as Actual_Proceeds,
ps.Qty * positions.Price as Actual_Cost, 
(ps.Qty * sales.Price) - (ps.Qty * positions.Price) as GainsLosses
FROM sales
LEFT JOIN position_sales as ps on ps.Sale_Id = sales.Id
LEFT JOIN positions on ps.Position_Id = positions.Id
WHERE  sales.Order_Date >= '2023-01-01 00:00:00'
ORDER BY sales.Coin, sales.Order_Date asc