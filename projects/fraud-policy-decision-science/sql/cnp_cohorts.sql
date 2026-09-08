-- Full settled denominators within CNP / non-CNP and transaction week.
SELECT CAST(transaction_day / 7 AS INTEGER) AS week,
       CASE WHEN cnp = 1 THEN 'CNP' ELSE 'Non-CNP' END AS payment_type,
       COUNT(*) AS transactions,
       SUM(amount) AS settled_value,
       SUM(fraud) AS fraud_count,
       SUM(CASE WHEN recognition_day-transaction_day <= :horizon THEN net ELSE 0 END)
           / SUM(amount) AS fixed_window_net_rate,
       SUM(CASE WHEN recognition_day <= :as_of THEN net ELSE 0 END)
           / SUM(amount) AS asof_net_rate,
       CASE WHEN MAX(transaction_day) + :horizon <= :as_of THEN 1 ELSE 0 END AS mature
FROM transactions
GROUP BY CAST(transaction_day / 7 AS INTEGER), cnp
ORDER BY week, payment_type;
