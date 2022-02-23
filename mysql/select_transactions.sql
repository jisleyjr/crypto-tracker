SELECT DATE_FORMAT(created_at, "%Y-%m") as 'created_month', market, transaction_type, AVG(price), SUM(amount), SUM(total), SUM(fee)
FROM homestead.transactions
WHERE market = 'ETHUSD'
GROUP BY created_month, market, transaction_type
order by created_month desc, transaction_type desc

/*SELECT DISTINCT market from `transactions` */