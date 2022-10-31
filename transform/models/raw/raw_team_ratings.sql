{{
    config(
        materialized = "ephemeral" if target.name == 'parquet' else "view"
) }}

SELECT *
FROM {{ source('nba', 'team_ratings' ) }}