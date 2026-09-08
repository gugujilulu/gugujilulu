-- Dashboard numerator and denominator have distinct clocks.
WITH numerator AS (
 SELECT CAST(recognition_day/7 AS INTEGER) AS week, SUM(net) AS recognized_net
 FROM transactions WHERE recognition_day <= :as_of GROUP BY 1
), denominator AS (
 SELECT CAST(transaction_day/7 AS INTEGER) AS week, SUM(amount) AS settled_value
 FROM transactions GROUP BY 1
)
SELECT d.week, COALESCE(n.recognized_net,0) / d.settled_value AS recognition_rate
FROM denominator d LEFT JOIN numerator n ON d.week=n.week ORDER BY d.week;
