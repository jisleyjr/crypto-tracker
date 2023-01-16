SELECT Coin, SUM(Remaining_Qty) as Total_Remaining, 
SUM(Remaining_Qty * Price) as Total_Cost, 
(SUM(Remaining_Qty * Price)/SUM(Remaining_Qty)) as Average_Cost
FROM `crypto-tracker`.positions
WHERE Remaining_Qty > 0.0
GROUP BY Coin
ORDER BY Coin ASC