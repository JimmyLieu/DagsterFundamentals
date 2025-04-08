## What is an Asset? 
## Data that requires management for accuracy, up-to-date

## Assets can take various forms including database table or view, file(local machine or AWS S3), ML model, and more...

from dagster import (
    asset, 
    AssetExecutionContext,
    AssetIn,
    Definitions,
    define_asset_job,
    AssetSelection,
    ScheduleDefinition,
      )
from typing import List

@asset(key="my_awesome_first_asset", group_name="get_started")
def my_first_asset(context:AssetExecutionContext):
    """
    This is our first asset for testing purposes
    """
    print("this is a print message.")
    context.log.info("this is a log message.")
    return [1, 2, 3]

## needs context:AssetExecutionContext for log messages
## second asset now depends on the first asset because of `deps=[my_first_asset]`

@asset(ins={"upstream": AssetIn(key="my_awesome_first_asset")}, group_name="get_started")
def my_second_asset(context:AssetExecutionContext, upstream: List):
    """
    This is our second asset
    """
    data = upstream + [4, 5, 6]
    context.log.info(f"Output data is {data}")
    return data

@asset(ins={
    "first_upstream": AssetIn("my_awesome_first_asset"),
    "second_upstream": AssetIn("my_second_asset")
}, group_name="get_started")
def my_third_asset(
    context:AssetExecutionContext,
    first_upstream: List,
    second_upstream: List):
    """
    This is our third asset
    """
    data = {
        "first_asset": first_upstream,
        "second_asset": second_upstream,
        "third_asset": second_upstream + [7,8]
    }
    context.log.info(f"Output data is: {data}")
    return data


#Built an asset graph with 3 assets and managed its dependencies.
#Created group_names for better organization

defs = Definitions(
    assets=[my_first_asset,my_second_asset,my_third_asset],
    jobs=[
        define_asset_job(
            name="hello_dagster_job",
            selection=AssetSelection.groups("get_started"),
        )
    ],
    schedules=[
        ScheduleDefinition(
            name="hello_dagster_schedule",
            job_name="hello_dagster_job",
            cron_schedule="* * * * *",
            ##crontab.guru to get scheduling names
        )
    ]
)