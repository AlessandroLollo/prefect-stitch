"""Stitch credentials block"""
from prefect.blocks.core import Block
from pydantic import SecretStr


class StitchCredentials(Block):
    """
    Block used to manage authentication with Stitch.
    Args:
        access_token (SecretStr): The Access token to use to connect to Stitch.

    Example:
        Load stored Stitch credentials
        ```python
        from prefect_stitch.credentials import StitchCredentials
        stitch_credentials_block = StitchCredentials.load("BLOCK_NAME")
        ```
    """  # noqa E501

    access_token: SecretStr

    _block_type_name = "Stitch Credentials"

    _logo_url = "https://github.com/PrefectHQ/prefect/blob/main/docs/img/collections/stitch.png?raw=true"  # noqa
