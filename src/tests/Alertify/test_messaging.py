"""Test"""
import unittest
from unittest.mock import patch

from Alertify import gotify, messaging  # pylint: disable=import-error


class MessageHandlerTest(unittest.TestCase):
    """
    Tests for methods in the MessageHandler class.
    """

    @classmethod
    def setUpClass(cls):
        cls.messaging = messaging.MessageHandler(
            gotify.Gotify('http://localhost', '', '')
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('Alertify.gotify.Gotify.send_alert')
    def test_process(self, mock_send_alert):
        """Test"""
        mock_send_alert.return_value = {
            'status': 200,
            'reason': 'OK',
            'json': None,
        }

        self.assertDictEqual(
            self.messaging.process(
                {
                    'status': 'firing',
                    'labels': {},
                    'annotations': {},
                }
            ),
            {
                'status': 200,
                'reason': 'OK',
                'json': None,
            },
        )
