from typing import Any

import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="taxi_data")
def taxi_source() -> Any:
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net",
        },
        "resource_defaults": {
            "write_disposition": "replace",
        },
        "resources": [
            {
                "name": "rides",
                "endpoint": {
                    "path": "data_engineering_zoomcamp_api",
                    "paginator": {
                        "type": "page_number",
                        "base_page": 1,
                        "page_param": "page",
                        "total_path": None,
                    },
                },
            },
        ],
    }
    yield from rest_api_resources(config)


def load_taxi_data() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data",
    )

    load_info = pipeline.run(taxi_source())
    print(load_info)


if __name__ == "__main__":
    load_taxi_data()