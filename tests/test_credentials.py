from pydantic import SecretStr

from prefect_stitch.credentials import StitchCredentials


def test_credentials_construction():
    cred = StitchCredentials(access_token=SecretStr("foo"))

    assert cred.access_token.get_secret_value() == "foo"
