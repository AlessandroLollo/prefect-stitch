import pytest
import responses
from prefect import flow
from pydantic import SecretStr

from prefect_stitch.credentials import StitchCredentials
from prefect_stitch.exceptions import StitchAPIFailureException
from prefect_stitch.tasks import start_replication_job


def test_start_replication_job_fails():
    @flow(name="failing_flow")
    def test_flow():
        creds = StitchCredentials(access_token=SecretStr("foo"))
        return start_replication_job(credentials=creds, source_id=1234)

    with pytest.raises(StitchAPIFailureException):
        test_flow()


@responses.activate
def test_start_replication_job_succeed():
    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST, url=api_url, status=200, json={"job_name": "foo"}
    )

    @flow(name="succeeding_flow")
    def test_flow():
        creds = StitchCredentials(access_token=SecretStr("foo"))
        return start_replication_job(credentials=creds, source_id=1234)

    result = test_flow()

    assert result == {"job_name": "foo"}
