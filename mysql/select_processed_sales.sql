SELECT sales.Coin, sales.Order_id, sales.Order_Date as Sales_Date, sales.Total_Proceeds,
ps.Qty * sales.Price as Actual_Proceeds,
positions.Order_Date as Buy_Date, positions.Total_Cost,
ps.Qty * positions.Price as Actual_Cost
FROM sales
INNER JOIN position_sales as ps on ps.Sale_Id = sales.Id
INNER JOIN positions on ps.Position_Id = positions.Id
WHERE sales.Coin = 'FLUX'
ORDER BY sales.Order_Date desc