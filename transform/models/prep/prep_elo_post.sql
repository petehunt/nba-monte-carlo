{{
    config(
        materialized = "ephemeral" if target.name == 'parquet' else "view"
) }}

SELECT
    *,
    {{ var('latest_ratings') }} AS latest_ratings
FROM {{ source('nba', 'elo_post' ) }}