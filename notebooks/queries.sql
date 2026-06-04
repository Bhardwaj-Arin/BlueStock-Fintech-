-- Bluestock Mutual Fund Analytics � Operational SQL Queries
-- Generated for Day 2 Tasks Deliverables

-- 1. Top 5 Funds by Total Asset Under Management (AUM) equivalent
SELECT 
    f.amfi_code,
    f.scheme_name,
    f.fund_house,
    SUM(t.amount_inr) AS total_investment_inr
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
WHERE t.transaction_type IN ('SIP', 'Lumpsum')
GROUP BY f.amfi_code, f.scheme_name, f.fund_house
ORDER BY total_investment_inr DESC
LIMIT 5;


-- 2. Average NAV Price Per Month for each fund scheme
SELECT 
    f.scheme_name,
    d.year,
    d.month,
    ROUND(AVG(n.nav), 4) AS average_monthly_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.date = d.date
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;


-- 3. Total Transactions and volume aggregated by State geography
SELECT 
    t.state,
    COUNT(t.transaction_id) AS total_transaction_count,
    ROUND(SUM(t.amount_inr), 2) AS total_volume_inr
FROM fact_transactions t
GROUP BY t.state
ORDER BY total_volume_inr DESC;


-- 4. Mutual Funds with low expense ratio profiles (Expense Ratio < 1%)
-- Note: Mapped from our cleaned scheme performance table definitions
SELECT 
    amfi_code,
    scheme_name,
    category,
    sub_category,
    expense_ratio
FROM cleaned_scheme_performance
WHERE expense_ratio < 1.0
ORDER BY expense_ratio ASC;


-- 5. KYC Status distribution breakdown among transacting investors
SELECT 
    t.kyc_status,
    COUNT(DISTINCT t.investor_id) AS total_unique_investors,
    COUNT(t.transaction_id) AS total_transaction_actions
FROM fact_transactions t
GROUP BY t.kyc_status;


-- 6. Total Redemption volume vs Investment volume breakdown
SELECT 
    t.transaction_type,
    COUNT(t.transaction_id) AS action_count,
    ROUND(SUM(t.amount_inr), 2) AS total_cash_flow_inr
FROM fact_transactions t
GROUP BY t.transaction_type;


-- 7. Heavy-volume investment transactions (Transactions above 5 Lakhs INR)
SELECT 
    transaction_id,
    investor_id,
    amfi_code,
    transaction_type,
    amount_inr,
    state
FROM fact_transactions
WHERE amount_inr > 500000
ORDER BY amount_inr DESC;


-- 8. Scheme count grouped by risk categories
SELECT 
    risk_category,
    COUNT(amfi_code) AS total_schemes
FROM dim_fund
GROUP BY risk_category
ORDER BY total_schemes DESC;


-- 9. Month-on-Month total transaction volume growth tracking
SELECT 
    d.year,
    d.month,
    COUNT(t.transaction_id) AS transaction_count,
    ROUND(SUM(t.amount_inr), 2) AS monthly_volume_inr
FROM fact_transactions t
JOIN dim_date d ON t.transaction_date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 10. High-activity cities ranked by unique customer count
SELECT 
    t.state,
    t.city,
    COUNT(DISTINCT t.investor_id) AS unique_investor_count
FROM fact_transactions t
GROUP BY t.state, t.city
ORDER BY unique_investor_count DESC
LIMIT 10;
