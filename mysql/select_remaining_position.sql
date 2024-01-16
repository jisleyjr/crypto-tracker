SELECT Order_Date, Coin, Original_Qty, Remaining_Qty, Price 
FROM `crypto-tracker`.positions
WHERE Remaining_Qty > 0
ORDER BY Coin asc, Order_Date asc;