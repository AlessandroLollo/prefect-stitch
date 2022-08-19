"""
Collection of tasks to interact with Stitch APIs.
In order to use Stitch APIs, you'll need to have
a Stitch Unlimited Plan or higher.
For further information, checkout [Stitch pricing](https://www.stitchdata.com/pricing/).
"""

from typing import Dict

from prefect import task

from prefect_stitch.credentials import StitchCredentials
from prefect_stitch.stitch_client import StitchClient


@task
def start_replication_job(credentials: StitchCredentials, source_id: int) -> Dict:
    """
    This task starts a new Stitch replication job using the provided source.

    Args:
        access_token: API access token that will be used to authenticate API calls.
        source_id: integer identifier of the source that will
            be used in the replication job.

    Returns:
        Replication job API JSON response.
    """
    stitch_client = StitchClient(credentials=credentials)
    return stitch_client.start_replication_job(source_id=source_id)
