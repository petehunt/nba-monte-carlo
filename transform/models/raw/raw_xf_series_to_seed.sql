{{
    config(
        materialized = "ephemeral" if target.name == 'parquet' else "view"
) }}

SELECT *
FROM {{ source('nba', 'xf_series_to_seed' ) }}