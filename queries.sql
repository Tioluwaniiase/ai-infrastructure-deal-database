-- Query 1: Capex per kW across the whole database, generation vs data center
-- The chart from the essay: two different assets, one metric
SELECT name, 'generation' AS asset_class, capex_per_kw, capex_flag
FROM ppa_deals WHERE capex_per_kw IS NOT NULL
UNION ALL
SELECT name, 'data center', capex_per_kw, capex_flag
FROM financing_deals WHERE capex_per_kw IS NOT NULL
ORDER BY capex_per_kw DESC;

-- Query 2: Contracted duration across the database
-- How many years of the physical layer are already locked up
SELECT name, term_years AS years, 'PPA' AS kind FROM ppa_deals WHERE term_years IS NOT NULL
UNION ALL
SELECT name, lease_term_years, 'Lease' FROM financing_deals WHERE lease_term_years IS NOT NULL
ORDER BY years DESC;

-- Query 3: Data provenance audit
-- The integrity check: how much of the database is disclosed vs estimated
SELECT capex_flag, COUNT(*) AS deals
FROM (
    SELECT capex_flag FROM ppa_deals WHERE capex_flag IS NOT NULL
    UNION ALL
    SELECT capex_flag FROM financing_deals WHERE capex_flag IS NOT NULL
)
GROUP BY capex_flag ORDER BY deals DESC;

-- Query 4: M&A buyer mix, strategic vs financial capital
-- Who is consolidating the generators
SELECT buyer_type, COUNT(*) AS deals, ROUND(SUM(equity_value_b), 1) AS total_equity_value_b
FROM ma_deals GROUP BY buyer_type;

-- Query 5: The credit support register
-- The essay's thesis in a query: every financing, and who stands behind it
SELECT name, ROUND(COALESCE(total_b, asset_value_b), 1) AS size_b,
       lease_term_years AS lease_yrs, credit_support
FROM financing_deals ORDER BY size_b DESC;
