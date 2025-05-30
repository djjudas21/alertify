"""
Module to handle communication with the Gotify server
"""
import json
import logging
import socket
from typing import Optional

from requests import request


class Gotify:
    """
    Class to handle Gotify communications
    """

    def __init__(self, url_prefix: str, app_key: str, client_key: Optional[str] = None):
        self.url_prefix = url_prefix
        self.app_key = app_key
        self.client_key = client_key
        self.base_headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
        }

    def _call(self, method: str, url: str, data: Optional[object] = None) -> dict:
        """
        Method to call Gotify with an app or client key as appropriate
        """
        headers = self.base_headers.copy()
        if method in ['GET', 'DELETE']:
            headers['X-Gotify-Key'] = self.client_key
        else:
            headers['X-Gotify-Key'] = self.app_key

        logging.debug('Sending to Gotify:\n%s', data)

        try:
            response = request(
                method,
                f'{self.url_prefix}{url}',
                json=data,
                headers=headers,
            )
        except (ConnectionRefusedError, socket.gaierror) as error:
            logging.error('Connection error: %s', error)
            return {
                'status': error.errno,
                'reason': error.strerror,
            }

        resp_obj = {
            'status': response.status_code,
            'reason': response.reason,
            'json': None,
        }
        if len(response.content) > 0:
            try:
                resp_obj['json'] = json.loads(response.content.decode())
            except json.decoder.JSONDecodeError as error:
                logging.error('Could not parse JSON: %s', error)

        logging.debug('Returned from Gotify:\n%s', json.dumps(resp_obj, indent=2))
        logging.debug('Status: %s, Reason: %s', resp_obj['status'], resp_obj['reason'])

        return resp_obj

    def delete(self, msg_id: str) -> dict:
        """
        Method to delete a message from the Gotify server
        """
        logging.debug('Deleting message ID: %s', msg_id)
        return self._call('DELETE', f'/message/{msg_id}')

    def find_byfingerprint(self, message: str) -> list:
        """
        Method to return the ID of a matching message
        """
        try:
            new_fingerprint = message['fingerprint']
        except KeyError:
            logging.debug('No fingerprint found in new message')
            return list()

        msg_list = []
        for old_message in self.messages():
            try:
                old_fingerprint = old_message['extras']['alertify']['fingerprint']
                if old_fingerprint == new_fingerprint:
                    msg_list.append(old_message['id'])
            except KeyError:
                logging.warning(
                    'No fingerprint found in message ID: %s',
                    old_message['id'],
                )

        return msg_list

    def messages(self) -> dict:
        """
        Method to return a list of messages from the Gotify server
        """
        if not self.client_key:
            logging.warning(
                'No client key is configured.  No messages could be retrieved.'
            )
            return dict()
        logging.debug('Fetching existing messages from Gotify')
        return self._call('GET', '/message')['json'].get('messages', [])

    def send_alert(self, payload: dict) -> dict:
        """
        Method to send a message payload to a Gotify server
        """
        logging.debug('Sending message to Gotify')
        return self._call('POST', '/message', data=payload)

    def healthcheck(self) -> dict:
        """
        Method to perform a healthcheck against Gotify
        """
        return self._call('GET', '/health')
