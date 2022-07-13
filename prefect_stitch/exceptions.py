"""
Exceptions to be used when interacting with Stitch APIs.
"""


class StitchAPIFailureException(Exception):
    """
    Exception to raise when a Stitch API return a response code != 200.
    """

    pass
