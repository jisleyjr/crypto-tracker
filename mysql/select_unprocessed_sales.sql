SELECT Id, Order_Date, Coin, Qty
FROM sales
WHERE Coin = 'Flux' and Processed = 0
ORDER BY Order_Date

/*
SELECT Id, Order_Date, Remaining_Qty
FROM positions
WHERE Coin = 'Flux' and Remaining_Qty > 0 and Order_Date <= '2022-08-25 04:57:04'

*/
