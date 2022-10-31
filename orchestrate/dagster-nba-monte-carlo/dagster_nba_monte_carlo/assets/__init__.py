from dagster import multi_asset, AssetOut, with_resources, AssetKey
import subprocess
import json
import os
from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource

CWD = os.path.join(os.path.dirname(__file__), "../../../..")

dbt_assets = with_resources(
    load_assets_from_dbt_project(
        project_dir=os.path.join(CWD, "transform"),
        profiles_dir=os.path.join(CWD, "transform", "profiles", "duckdb"),
        target_dir=os.path.join(CWD, "docs"),
    ),
    {
        "dbt": dbt_cli_resource.configured(
            {"project_dir": os.path.join(CWD, "transform")}
        )
    },
)

TAP = "tap-spreadsheets-anywhere"
TARGET = "target-parquet"

catalog = json.loads(
    subprocess.check_output(["meltano", "invoke", TAP, "--discover"], cwd=CWD)
)
outs = {
    stream["tap_stream_id"]: AssetOut(
        key=AssetKey(
            [
                "nba",
                "schedule"
                if stream["tap_stream_id"] == "nba_schedule_2023"
                else stream["tap_stream_id"],
            ]
        )
    )
    for stream in catalog["streams"]
}


@multi_asset(outs=outs, compute_kind="meltano")
def meltano_assets():
    subprocess.check_call(["meltano", "run", TAP, TARGET, "--full-refresh"], cwd=CWD)
    subprocess.check_call(
        ["awslocal", "s3", "sync", "/tmp/data_catalog/psa", "s3://datalake/psa"],
        cwd=CWD,
    )
    return (None,) * len(outs)
