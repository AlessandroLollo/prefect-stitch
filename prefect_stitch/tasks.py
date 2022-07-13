"""
Collection of tasks to interact with Stitch APIs.
"""

from typing import Dict

from prefect import task

from prefect_stitch.utils import StitchClient


@task
def start_replication_job(access_token: str, source_id: int) -> Dict:
    """
    This task starts a new Stitch replication job using the provided source.

    Args:
        access_token: API access token that will be used to authenticate API calls.
        source_id: integer identifier of the source that will
            be used in the replication job.

    Returns:
        Replication job API JSON response.
    """
    stitch_client = StitchClient(access_token=access_token)
    return stitch_client.start_replication_job(source_id=source_id)
