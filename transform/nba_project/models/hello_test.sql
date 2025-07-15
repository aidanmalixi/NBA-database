{{ config(materialized='table') }}

SELECT
    'hello' AS message,
    current_timestamp AS created_at