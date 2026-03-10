-- ============================================================
-- RetailPulse 360 — SQL Database Schema & Analytical Queries
-- Database: PostgreSQL 15+
-- Author: NovaMart Data Analytics Team
-- ============================================================

-- ─────────────────────────────────────────────
-- SECTION 1: DATABASE SETUP
-- ─────────────────────────────────────────────

CREATE DATABASE retailpulse360;
\c retailpulse360;

-- ─────────────────────────────────────────────
-- SECTION 2: DIMENSION TABLES (Star Schema)
-- ─────────────────────────────────────────────

-- DIM: Stores
CREATE TABLE dim_stores (
    store_id        VARCHAR(10)  PRIMARY KEY,
    store_name      VARCHAR(100) NOT NULL,
    city            VARCHAR(60),
    region          VARCHAR(30),
    store_type      VARCHAR(30),
    open_date       DATE,
    sqft            INTEGER,
    num_employees   INTEGER,
    manager         VARCHAR(100),
    monthly_rent    NUMERIC(10,2)
);

-- DIM: Products
CREATE TABLE dim_products (
    product_id      VARCHAR(10)  PRIMARY KEY,
    product_name    VARCHAR(150) NOT NULL,
    category        VARCHAR(60),
    subcategory     VARCHAR(60),
    brand           VARCHAR(60),
    unit_cost       NUMERIC(10,2),
    unit_price      NUMERIC(10,2),
    margin_pct      NUMERIC(5,2),
    supplier        VARCHAR(60),
    reorder_level   INTEGER,
    weight_kg       NUMERIC(6,2)
);

-- DIM: Customers
CREATE TABLE dim_customers (
    customer_id         VARCHAR(10)  PRIMARY KEY,
    first_name          VARCHAR(50),
    last_name           VARCHAR(50),
    email               VARCHAR(100),
    age                 INTEGER,
    gender              VARCHAR(10),
    city                VARCHAR(60),
    registration_date   DATE,
    loyalty_tier        VARCHAR(20),
    email_opt_in        BOOLEAN
);

-- DIM: Date (Calendar table — critical for time intelligence)
CREATE TABLE dim_date (
    date_id         DATE         PRIMARY KEY,
    year            INTEGER,
    quarter         INTEGER,
    month           INTEGER,
    month_name      VARCHAR(15),
    week            INTEGER,
    day_of_week     INTEGER,
    day_name        VARCHAR(15),
    is_weekend      BOOLEAN,
    is_holiday      BOOLEAN DEFAULT FALSE,
    fiscal_year     INTEGER,
    fiscal_quarter  INTEGER
);

-- Populate dim_date for 2022–2025
INSERT INTO dim_date
SELECT
    d::DATE                             AS date_id,
    EXTRACT(YEAR FROM d)                AS year,
    EXTRACT(QUARTER FROM d)             AS quarter,
    EXTRACT(MONTH FROM d)               AS month,
    TO_CHAR(d, 'Month')                 AS month_name,
    EXTRACT(WEEK FROM d)                AS week,
    EXTRACT(DOW FROM d)                 AS day_of_week,
    TO_CHAR(d, 'Day')                   AS day_name,
    EXTRACT(DOW FROM d) IN (0,6)        AS is_weekend,
    FALSE                               AS is_holiday,
    EXTRACT(YEAR FROM d)                AS fiscal_year,
    EXTRACT(QUARTER FROM d)             AS fiscal_quarter
FROM generate_series('2022-01-01'::DATE, '2025-12-31'::DATE, '1 day') d;

-- ─────────────────────────────────────────────
-- SECTION 3: FACT TABLES
-- ─────────────────────────────────────────────

-- FACT: Transactions
CREATE TABLE fact_transactions (
    transaction_id      VARCHAR(15)  PRIMARY KEY,
    date                DATE         NOT NULL,
    store_id            VARCHAR(10)  REFERENCES dim_stores(store_id),
    customer_id         VARCHAR(10)  REFERENCES dim_customers(customer_id),
    product_id          VARCHAR(10)  REFERENCES dim_products(product_id),
    quantity            INTEGER,
    unit_price          NUMERIC(10,2),
    discount_amount     NUMERIC(10,2),
    final_unit_price    NUMERIC(10,2),
    total_revenue       NUMERIC(12,2),
    total_cost          NUMERIC(12,2),
    gross_profit        NUMERIC(12,2),
    payment_method      VARCHAR(30),
    channel             VARCHAR(20),
    FOREIGN KEY (date) REFERENCES dim_date(date_id)
);

-- FACT: Inventory (snapshot)
CREATE TABLE fact_inventory (
    inventory_id    SERIAL       PRIMARY KEY,
    store_id        VARCHAR(10)  REFERENCES dim_stores(store_id),
    product_id      VARCHAR(10)  REFERENCES dim_products(product_id),
    qty_on_hand     INTEGER,
    reorder_level   INTEGER,
    last_restocked  DATE,
    status          VARCHAR(20),
    snapshot_date   DATE DEFAULT CURRENT_DATE
);

-- FACT: Reviews
CREATE TABLE fact_reviews (
    review_id       VARCHAR(10)  PRIMARY KEY,
    transaction_id  VARCHAR(15)  REFERENCES fact_transactions(transaction_id),
    customer_id     VARCHAR(10)  REFERENCES dim_customers(customer_id),
    product_id      VARCHAR(10)  REFERENCES dim_products(product_id),
    store_id        VARCHAR(10)  REFERENCES dim_stores(store_id),
    review_date     DATE,
    rating          INTEGER CHECK (rating BETWEEN 1 AND 5),
    sentiment       VARCHAR(20),
    review_text     TEXT
);

-- ─────────────────────────────────────────────
-- SECTION 4: INDEXES FOR PERFORMANCE
-- ─────────────────────────────────────────────

CREATE INDEX idx_trans_date      ON fact_transactions(date);
CREATE INDEX idx_trans_store     ON fact_transactions(store_id);
CREATE INDEX idx_trans_customer  ON fact_transactions(customer_id);
CREATE INDEX idx_trans_product   ON fact_transactions(product_id);
CREATE INDEX idx_reviews_store   ON fact_reviews(store_id);
CREATE INDEX idx_inv_store       ON fact_inventory(store_id);

-- ─────────────────────────────────────────────
-- SECTION 5: VIEWS (Pre-built for Power BI)
-- ─────────────────────────────────────────────

-- View: Monthly Revenue Summary
CREATE OR REPLACE VIEW vw_monthly_revenue AS
SELECT
    d.year,
    d.month,
    d.month_name,
    s.region,
    s.store_type,
    SUM(t.total_revenue)   AS total_revenue,
    SUM(t.total_cost)      AS total_cost,
    SUM(t.gross_profit)    AS gross_profit,
    COUNT(DISTINCT t.transaction_id) AS num_transactions,
    COUNT(DISTINCT t.customer_id)    AS unique_customers,
    ROUND(SUM(t.gross_profit) / NULLIF(SUM(t.total_revenue),0) * 100, 2) AS gp_margin_pct
FROM fact_transactions t
JOIN dim_date    d ON t.date = d.date_id
JOIN dim_stores  s ON t.store_id = s.store_id
GROUP BY d.year, d.month, d.month_name, s.region, s.store_type;

-- View: Product Performance
CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    p.brand,
    SUM(t.quantity)                AS units_sold,
    SUM(t.total_revenue)           AS total_revenue,
    SUM(t.gross_profit)            AS total_profit,
    ROUND(AVG(t.final_unit_price), 2) AS avg_selling_price,
    ROUND(SUM(t.gross_profit)/NULLIF(SUM(t.total_revenue),0)*100, 2) AS margin_pct
FROM fact_transactions t
JOIN dim_products p ON t.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.subcategory, p.brand;

-- View: Customer 360 (RFM base)
CREATE OR REPLACE VIEW vw_customer_rfm AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name  AS customer_name,
    c.loyalty_tier,
    c.age,
    c.gender,
    MAX(t.date)                          AS last_purchase_date,
    CURRENT_DATE - MAX(t.date)           AS recency_days,
    COUNT(DISTINCT t.transaction_id)     AS frequency,
    SUM(t.total_revenue)                 AS monetary_value,
    ROUND(AVG(t.total_revenue), 2)       AS avg_order_value
FROM dim_customers c
LEFT JOIN fact_transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, customer_name, c.loyalty_tier, c.age, c.gender;

-- View: Store Scorecard
CREATE OR REPLACE VIEW vw_store_scorecard AS
SELECT
    s.store_id,
    s.store_name,
    s.region,
    s.store_type,
    s.num_employees,
    s.monthly_rent,
    SUM(t.total_revenue)    AS total_revenue,
    SUM(t.gross_profit)     AS total_profit,
    COUNT(DISTINCT t.customer_id) AS unique_customers,
    COUNT(DISTINCT t.transaction_id) AS total_transactions,
    ROUND(SUM(t.total_revenue) / NULLIF(s.num_employees,0), 0) AS revenue_per_employee,
    ROUND(SUM(t.total_revenue) / NULLIF(s.monthly_rent,0), 2) AS revenue_to_rent_ratio
FROM dim_stores s
LEFT JOIN fact_transactions t ON s.store_id = t.store_id
GROUP BY s.store_id, s.store_name, s.region, s.store_type, s.num_employees, s.monthly_rent;

-- ─────────────────────────────────────────────
-- SECTION 6: ANALYTICAL QUERIES
-- ─────────────────────────────────────────────

-- Q1: Year-over-Year Revenue Comparison
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(t.total_revenue)  AS current_revenue,
    LAG(SUM(t.total_revenue)) OVER (PARTITION BY d.month ORDER BY d.year) AS prev_year_revenue,
    ROUND(
        (SUM(t.total_revenue) - LAG(SUM(t.total_revenue)) OVER (PARTITION BY d.month ORDER BY d.year))
        / NULLIF(LAG(SUM(t.total_revenue)) OVER (PARTITION BY d.month ORDER BY d.year), 0) * 100, 2
    ) AS yoy_growth_pct
FROM fact_transactions t
JOIN dim_date d ON t.date = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Q2: Top 10 Revenue-Generating Products (with rank)
SELECT
    RANK() OVER (ORDER BY SUM(t.total_revenue) DESC) AS revenue_rank,
    p.product_name,
    p.category,
    SUM(t.total_revenue)  AS total_revenue,
    SUM(t.quantity)       AS units_sold,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM fact_transactions t
JOIN dim_products  p ON t.product_id = p.product_id
LEFT JOIN fact_reviews r ON t.product_id = r.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- Q3: Customer RFM Segmentation
WITH rfm AS (
    SELECT
        customer_id,
        CURRENT_DATE - MAX(date)           AS recency,
        COUNT(DISTINCT transaction_id)      AS frequency,
        SUM(total_revenue)                  AS monetary
    FROM fact_transactions
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency DESC)    AS r_score,
        NTILE(5) OVER (ORDER BY frequency)        AS f_score,
        NTILE(5) OVER (ORDER BY monetary)         AS m_score
    FROM rfm
)
SELECT
    customer_id,
    recency, frequency, monetary,
    r_score, f_score, m_score,
    (r_score + f_score + m_score)  AS rfm_total,
    CASE
        WHEN (r_score + f_score + m_score) >= 13 THEN 'Champions'
        WHEN (r_score + f_score + m_score) >= 10 THEN 'Loyal Customers'
        WHEN (r_score + f_score + m_score) >= 7  THEN 'Potential Loyalists'
        WHEN r_score >= 4 AND (f_score + m_score) <= 4 THEN 'New Customers'
        WHEN r_score <= 2 AND (f_score + m_score) >= 8 THEN 'At Risk'
        ELSE 'Hibernating'
    END AS rfm_segment
FROM rfm_scores
ORDER BY rfm_total DESC;

-- Q4: Store Performance Ranking with Running Total
SELECT
    s.region,
    s.store_name,
    SUM(t.total_revenue)  AS store_revenue,
    RANK() OVER (PARTITION BY s.region ORDER BY SUM(t.total_revenue) DESC) AS region_rank,
    SUM(SUM(t.total_revenue)) OVER (PARTITION BY s.region ORDER BY SUM(t.total_revenue) DESC) AS running_regional_total
FROM fact_transactions t
JOIN dim_stores s ON t.store_id = s.store_id
WHERE EXTRACT(YEAR FROM t.date) = 2024
GROUP BY s.region, s.store_name
ORDER BY s.region, store_revenue DESC;

-- Q5: Product Basket Analysis (frequently bought together)
SELECT
    a.product_id AS product_a,
    b.product_id AS product_b,
    COUNT(*) AS co_purchase_count
FROM fact_transactions a
JOIN fact_transactions b
    ON a.customer_id = b.customer_id
    AND a.date = b.date
    AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY co_purchase_count DESC
LIMIT 20;

-- Q6: Customer Churn Risk (no purchase in 90+ days)
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.loyalty_tier,
    MAX(t.date)                         AS last_purchase,
    CURRENT_DATE - MAX(t.date)          AS days_since_purchase,
    COUNT(DISTINCT t.transaction_id)    AS lifetime_orders,
    SUM(t.total_revenue)               AS lifetime_value,
    CASE
        WHEN CURRENT_DATE - MAX(t.date) > 180 THEN 'High Risk'
        WHEN CURRENT_DATE - MAX(t.date) > 90  THEN 'Medium Risk'
        ELSE 'Active'
    END AS churn_risk
FROM dim_customers c
JOIN fact_transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id, customer_name, c.loyalty_tier
HAVING CURRENT_DATE - MAX(t.date) > 60
ORDER BY days_since_purchase DESC;

-- Q7: Inventory Reorder Alert
SELECT
    i.store_id,
    s.store_name,
    s.region,
    p.product_name,
    p.category,
    i.qty_on_hand,
    i.reorder_level,
    i.status,
    i.last_restocked,
    CURRENT_DATE - i.last_restocked AS days_since_restock
FROM fact_inventory i
JOIN dim_stores   s ON i.store_id = s.store_id
JOIN dim_products p ON i.product_id = p.product_id
WHERE i.qty_on_hand <= i.reorder_level
ORDER BY i.qty_on_hand ASC;

-- Q8: Weekly Revenue Trend with 4-Week Moving Average
SELECT
    d.year,
    d.week,
    SUM(t.total_revenue) AS weekly_revenue,
    ROUND(AVG(SUM(t.total_revenue)) OVER (
        ORDER BY d.year, d.week ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ), 2) AS moving_avg_4w
FROM fact_transactions t
JOIN dim_date d ON t.date = d.date_id
GROUP BY d.year, d.week
ORDER BY d.year, d.week;

-- Q9: Sentiment vs Sales Performance
SELECT
    s.store_name,
    s.region,
    COUNT(CASE WHEN r.sentiment = 'Positive' THEN 1 END) AS positive_reviews,
    COUNT(CASE WHEN r.sentiment = 'Neutral'  THEN 1 END) AS neutral_reviews,
    COUNT(CASE WHEN r.sentiment = 'Negative' THEN 1 END) AS negative_reviews,
    ROUND(AVG(r.rating), 2)   AS avg_rating,
    SUM(t.total_revenue)      AS total_revenue,
    ROUND(
        COUNT(CASE WHEN r.sentiment = 'Positive' THEN 1 END) * 100.0 / NULLIF(COUNT(r.review_id), 0),
        1
    ) AS positive_rate_pct
FROM fact_reviews r
JOIN fact_transactions t ON r.transaction_id = t.transaction_id
JOIN dim_stores s         ON r.store_id = s.store_id
GROUP BY s.store_name, s.region
ORDER BY positive_rate_pct DESC;

-- Q10: Stored Procedure — Monthly Executive KPI Report
CREATE OR REPLACE FUNCTION sp_monthly_kpi(p_year INT, p_month INT)
RETURNS TABLE (
    kpi_name    TEXT,
    kpi_value   NUMERIC,
    kpi_unit    TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'Total Revenue'::TEXT,        ROUND(SUM(total_revenue)::NUMERIC, 0),  '$'
    FROM fact_transactions
    WHERE EXTRACT(YEAR FROM date) = p_year AND EXTRACT(MONTH FROM date) = p_month
    UNION ALL
    SELECT 'Total Gross Profit',         ROUND(SUM(gross_profit)::NUMERIC, 0),   '$'
    FROM fact_transactions
    WHERE EXTRACT(YEAR FROM date) = p_year AND EXTRACT(MONTH FROM date) = p_month
    UNION ALL
    SELECT 'GP Margin %',                ROUND(SUM(gross_profit)/NULLIF(SUM(total_revenue),0)*100, 2), '%'
    FROM fact_transactions
    WHERE EXTRACT(YEAR FROM date) = p_year AND EXTRACT(MONTH FROM date) = p_month
    UNION ALL
    SELECT 'Unique Customers',           COUNT(DISTINCT customer_id)::NUMERIC,    'count'
    FROM fact_transactions
    WHERE EXTRACT(YEAR FROM date) = p_year AND EXTRACT(MONTH FROM date) = p_month
    UNION ALL
    SELECT 'Total Transactions',         COUNT(DISTINCT transaction_id)::NUMERIC, 'count'
    FROM fact_transactions
    WHERE EXTRACT(YEAR FROM date) = p_year AND EXTRACT(MONTH FROM date) = p_month
    UNION ALL
    SELECT 'Avg Order Value',            ROUND(AVG(total_revenue)::NUMERIC, 2),   '$'
    FROM fact_transactions
    WHERE EXTRACT(YEAR FROM date) = p_year AND EXTRACT(MONTH FROM date) = p_month;
END;
$$ LANGUAGE plpgsql;

-- Usage: SELECT * FROM sp_monthly_kpi(2024, 12);

-- ─────────────────────────────────────────────
-- SECTION 7: IMPORT COMMANDS (psql)
-- ─────────────────────────────────────────────

/*
\COPY dim_stores     FROM 'data/stores.csv'       CSV HEADER;
\COPY dim_products   FROM 'data/products.csv'     CSV HEADER;
\COPY dim_customers  FROM 'data/customers.csv'    CSV HEADER;
\COPY fact_transactions FROM 'data/transactions.csv' CSV HEADER;
\COPY fact_inventory FROM 'data/inventory.csv'    CSV HEADER;
\COPY fact_reviews   FROM 'data/reviews.csv'      CSV HEADER;
*/
