"""
Module for handling any healthcheck related activity
"""
from typing import Tuple

from .gotify import Gotify


class Healthcheck:
    """
    Class to handle the healthchecks
    """

    def __init__(self, gotify_client: Gotify):
        self.gotify = gotify_client

    def gotify_alive(self) -> Tuple[str, int]:
        """
        Simple method to return the Gotify healthcheck response
        """
        return self.gotify.healthcheck()
