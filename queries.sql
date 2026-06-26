-- 1. Top 5 Funds by AUM
SELECT fund_house, MAX(aum_amount) as total_aum 
FROM fact_aum 
GROUP BY fund_house 
ORDER BY total_aum DESC 
LIMIT 5;

-- 2. Average NAV per Month
SELECT STRFTIME('%Y-%m', date) as year_month, AVG(nav) as avg_nav 
FROM fact_nav 
GROUP BY year_month 
ORDER BY year_month;

-- 3. Total Transaction Volume by State
SELECT state, SUM(amount) as total_invested, COUNT(transaction_id) as total_txs
FROM fact_transactions
GROUP BY state
ORDER BY total_invested DESC;

-- 4. Low-Expense Mutual Funds (< 1%)
SELECT f.scheme_name, p.expense_ratio 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0;

-- 5. Total Redemption Outflows vs Inflows
SELECT transaction_type, SUM(amount) as volume 
FROM fact_transactions 
GROUP BY transaction_type;