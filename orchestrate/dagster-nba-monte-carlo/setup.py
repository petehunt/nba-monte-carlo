from setuptools import find_packages, setup

setup(
    name="dagster_nba_monte_carlo",
    packages=find_packages(exclude=["dagster_nba_monte_carlo_tests"]),
    install_requires=["dagster", "dagster-dbt", "dbt-duckdb"],
    extras_require={"dev": ["dagit", "pytest"]},
)
