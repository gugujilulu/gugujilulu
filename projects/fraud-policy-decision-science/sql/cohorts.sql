-- Entire occurrence population, common 42-day window, as-of day 210.
-- Observed recent cohorts have less follow-up; compare mature cohorts separately.
SELECT CAST(transaction_day / 7 AS INTEGER) AS week,
       COUNT(*) AS transactions, SUM(amount) AS settled_value,
       SUM(CASE WHEN recognition_day <= :as_of THEN net ELSE 0 END) / SUM(amount) AS naive_rate,
       SUM(CASE WHEN recognition_day-transaction_day <= :horizon THEN net ELSE 0 END) / SUM(amount) AS fixed_window_rate,
       CASE WHEN MAX(transaction_day) + :horizon <= :as_of THEN 1 ELSE 0 END AS mature
FROM transactions
GROUP BY CAST(transaction_day / 7 AS INTEGER)
ORDER BY week;
