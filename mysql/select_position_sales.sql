SELECT p.Coin, ps.Qty, p.Order_Date as Buy_Date, ps.Qty * p.Price as Cost, 
s.Order_Date as Sales_Date, ps.Qty * s.Price as Proceeds
FROM `crypto-tracker`.position_sales as ps
INNER JOIN positions as p ON p.Id = ps.Position_Id
INNER JOIN sales as s on s.Id = ps.Sale_Id
ORDER BY p.Coin asc, Sales_Date asc, Buy_Date asc;