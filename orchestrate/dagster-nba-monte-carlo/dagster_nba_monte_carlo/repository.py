from dagster import load_assets_from_package_module, repository

from dagster_nba_monte_carlo import assets


@repository
def dagster_nba_monte_carlo():
    return [load_assets_from_package_module(assets)]
