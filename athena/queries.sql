-- Create table (optional if Glue Crawler handles it)
CREATE EXTERNAL TABLE IF NOT EXISTS electricity_usage (
    record_id STRING,
    meter_id STRING,
    recorded_at TIMESTAMP,
    consumption_kWh DOUBLE,
    voltage FLOAT,
    current FLOAT
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://smart-meter-070525/data/'
TBLPROPERTIES ('has_encrypted_data'='false');

-- Query monthly usage per meter
SELECT
    meter_id,
    DATE_TRUNC('month', recorded_at) AS billing_month,
    SUM(consumption_kWh) AS total_consumption
FROM electricity_usage
GROUP BY meter_id, billing_month
ORDER BY billing_month DESC;

-- Detect anomalous spikes
SELECT *
FROM electricity_usage
WHERE consumption_kWh > 10
ORDER BY recorded_at DESC
LIMIT 50;
