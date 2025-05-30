"""
Module for handling the messaging
"""
import logging
from typing import Optional

from .gotify import Gotify


class MessageHandler:
    """
    Class to handle alert messaging
    """

    def __init__(
        self,
        gotify_client: Gotify,
        disable_resolved: Optional[bool] = False,
        delete_onresolve: Optional[bool] = False,
    ):
        self.gotify = gotify_client
        self.disable_resolved = disable_resolved
        self.delete_onresolve = delete_onresolve

    def process(self, alert: dict) -> dict:
        """
        Method to process the alert message
        """
        try:
            if alert['status'] == 'resolved':
                if self.disable_resolved:
                    logging.info('Ignoring resolved messages')
                    return {
                        'status': 200,
                        'reason': 'Ignored. "resolved" messages are disabled',
                    }

                if self.delete_onresolve:
                    for alert_id in self.gotify.find_byfingerprint(alert):
                        if not self.gotify.delete(alert_id):
                            logging.error(
                                'There was a problem removing message ID %d',
                                alert_id,
                            )
                    return {'status': 200, 'reason': 'Message deletion complete'}

                prefix = 'resolved'
            else:
                prefix = alert['labels'].get('severity', 'warning')

            instance = alert['labels'].get('instance', None)

            gotify_msg = {
                'title': '[{}] {}'.format(
                    prefix.upper(),
                    alert['annotations'].get('summary'),
                ),
                'message': '{}{}'.format(
                    f'{instance}: ' if instance else '',
                    alert['annotations'].get('description', ''),
                ),
                'priority': int(alert['labels'].get('priority', 5)),
                'extras': {
                    'alertify': {
                        'fingerprint': alert.get('fingerprint', None),
                    }
                },
            }
        except KeyError as error:
            logging.error('KeyError: %s', error)
            return {
                'status': 400,
                'reason': f'Missing field: {error}',
            }

        return self.gotify.send_alert(gotify_msg)
