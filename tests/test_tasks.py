import pytest
import responses
from prefect import flow

from prefect_stitch.exceptions import StitchAPIFailureException
from prefect_stitch.tasks import start_replication_job
from prefect_stitch.utils import StitchClient


def test_stitch_client_init():
    sc = StitchClient(access_token="abc")

    assert sc.access_token == "abc"


def test_run_without_source_id_raises():
    @flow(name="test_flow_1")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=None)

    msg_match = "To start a replication job, please provide the the source identifier"

    with pytest.raises(StitchAPIFailureException, match=msg_match):
        test_flow().result().result()


@responses.activate
def test_run_with_not_ok_status_code_raises():
    @flow(name="test_flow")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=1234)

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(method=responses.POST, url=api_url, status=123)

    msg_match = "There was an error while calling Stitch API"
    with pytest.raises(StitchAPIFailureException, match=msg_match):

        test_flow().result().result()


@responses.activate
def test_run_with_invalid_source_raises():
    @flow(name="test_flow_2")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=1234)

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST,
        url=api_url,
        status=400,
        json={
            "error": {
                "type": "invalid_source",
                "message": "Unable to locate source(1234) for client (<CLIENT_ID>)",
            }
        },
    )

    msg_match = "Stitch API responded with error: Unable to locate source"
    with pytest.raises(StitchAPIFailureException, match=msg_match):
        test_flow().result().result()


@responses.activate
def test_run_with_deleted_source_raises():
    @flow(name="test_flow_3")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=1234)

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST,
        url=api_url,
        status=400,
        json={
            "error": {"type": "invalid_source", "message": "Integration is deleted."}
        },
    )

    msg_match = "Stitch API responded with error: Integration is deleted."

    with pytest.raises(StitchAPIFailureException, match=msg_match):
        test_flow().result().result()


@responses.activate
def test_run_already_running_job_raises():
    @flow(name="test_flow_4")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=1234)

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST,
        url=api_url,
        status=200,
        json={
            "error": {
                "type": "already_running",
                "message": "Did not create job for client-id",
            }
        },
    )

    msg_match = "Stitch API responded with error: Did not create job for client-id"

    with pytest.raises(StitchAPIFailureException, match=msg_match):
        test_flow().result().result()


@responses.activate
def test_run_with_valid_source_check_auth_headers():
    @flow(name="test_flow_5")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=1234)

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST, url=api_url, status=200, json={"job_name": "foo"}
    )

    test_flow().result().result()

    assert responses.calls[0].request.headers["Authorization"] == "Bearer abc"


@responses.activate
def test_run_success():
    @flow(name="test_flow_6")
    def test_flow():
        return start_replication_job(access_token="abc", source_id=1234)

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST, url=api_url, status=200, json={"job_name": "foo"}
    )

    result = test_flow().result().result()

    assert result == {"job_name": "foo"}
