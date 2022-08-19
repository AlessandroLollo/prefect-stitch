"""
An object that can be used to interact with Stitch APIs.
"""

from typing import Dict, Optional

from requests import Session

from prefect_stitch.credentials import StitchCredentials
from prefect_stitch.exceptions import StitchAPIFailureException


class StitchClient:
    """
    Create a client that can be used to interact with Stitch APIs
    using the provided access token to authenticate API calls.

    Args:
        credentials: access token that will be used to
            authenticate API calls.
    """

    # Stitch API base url
    __STITCH_API_URL = "https://api.stitchdata.com"

    # Stitch API version
    __STITCH_API_VERSION = "v4"

    def __init__(self, credentials: StitchCredentials) -> None:
        self.credentials = credentials

    def __get_base_url(self) -> str:
        """
        Returns Stitch API base url.

        Returns:
            Stitch base URL.
        """
        return f"{self.__STITCH_API_URL}/{self.__STITCH_API_VERSION}"

    def __get_replication_job_url(self, source_id: int) -> str:
        """
        Returns the Replication Job API URL.

        Args:
            source_id: The integer identifier of the source that
                will be used in the replication job.

        Returns:
            Replication Job API URL.
        """
        return f"{self.__get_base_url()}/sources/{source_id}/sync"

    def __get_session(self) -> Session:
        """
        Returns a `requests.Session` object that can be used in subsequent API calls.

        Returns:
            Session object configured with the proper headers.
        """
        access_token = self.credentials.access_token.get_secret_value()
        session = Session()
        session.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        return session

    def __call_api(
        self, api_url: str, params: Optional[Dict], http_method: str
    ) -> Dict:
        """
        Make an API call to the URL using the specified parameters and HTTP method.

        Args:
            api_url: The URL of the API to call.
            params: Optional parameters to pass to the API call.
            http_method: String representing the HTTP method
                to use to make the API call.

        Raises:
            `StitchAPIFailureException` if the response code is not 200.
            `StitchAPIFailureException` if the response contains an error payload.

        Returns:
            The API JSON response.
        """

        session = self.__get_session()
        http_fn = session.get if http_method == "GET" else session.post
        with http_fn(url=api_url, params=params) as response:
            if response.status_code not in [200, 400]:
                err = f"There was an error while calling Stitch API: {response.reason}"
                raise StitchAPIFailureException(err)

            data = response.json()

            if "error" in data:
                err = data["error"]["message"]
                raise StitchAPIFailureException(
                    f"Stitch API responded with error: {err}"
                )

        return data

    def start_replication_job(self, source_id: int) -> Dict:
        """
        Start a replication job of the source.

        Args:
            source_id: The integer identifier of the source that
                will be used in the replication job.

        Returns:
            The replication job API JSON response.
        """
        if source_id is None:
            msg = "To start a replication job, please provide the the source identifier"
            raise StitchAPIFailureException(msg)
        return self.__call_api(
            api_url=self.__get_replication_job_url(source_id=source_id),
            params=None,
            http_method="POST",
        )
