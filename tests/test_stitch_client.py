import pytest
import responses
from pydantic import SecretStr

from prefect_stitch.credentials import StitchCredentials
from prefect_stitch.exceptions import StitchAPIFailureException
from prefect_stitch.stitch_client import StitchClient


def test_stitch_client_construction():

    client = StitchClient(credentials=StitchCredentials(access_token=SecretStr("foo")))

    assert client.credentials.access_token.get_secret_value() == "foo"


@responses.activate
def test_start_replication_job_raises():

    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(method=responses.POST, url=api_url, status=123)

    msg_match = "There was an error while calling Stitch API"
    with pytest.raises(StitchAPIFailureException, match=msg_match):
        creds = StitchCredentials(access_token=SecretStr("foo"))
        client = StitchClient(credentials=creds)

        client.start_replication_job(source_id=1234)


@responses.activate
def test_start_replication_job_with_invalid_source_raises():

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
        creds = StitchCredentials(access_token=SecretStr("foo"))
        client = StitchClient(credentials=creds)

        client.start_replication_job(source_id=1234)


@responses.activate
def test_start_replication_job_with_deleted_source_raises():
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
        creds = StitchCredentials(access_token=SecretStr("foo"))
        client = StitchClient(credentials=creds)

        client.start_replication_job(source_id=1234)


@responses.activate
def test_start_replication_job_already_running_raises():
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
        creds = StitchCredentials(access_token=SecretStr("foo"))
        client = StitchClient(credentials=creds)

        client.start_replication_job(source_id=1234)


@responses.activate
def test_start_replication_job_check_auth_headers():
    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST, url=api_url, status=200, json={"job_name": "foo"}
    )

    creds = StitchCredentials(access_token=SecretStr("foo"))
    client = StitchClient(credentials=creds)

    client.start_replication_job(source_id=1234)

    assert responses.calls[0].request.headers["Authorization"] == "Bearer foo"


@responses.activate
def test_start_replication_job_success():
    api_url = "https://api.stitchdata.com/v4/sources/1234/sync"
    responses.add(
        method=responses.POST, url=api_url, status=200, json={"job_name": "foo"}
    )

    creds = StitchCredentials(access_token=SecretStr("foo"))
    client = StitchClient(credentials=creds)

    result = client.start_replication_job(source_id=1234)

    assert result == {"job_name": "foo"}
