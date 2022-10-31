{{
    config(
        materialized = "ephemeral" if target.name == 'parquet' else "view"
) }}

SELECT *
FROM {{ source('nba', 'nba_elo_latest' ) }}