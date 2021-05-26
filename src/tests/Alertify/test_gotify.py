"""
Module to handle unit tests for the Alertify.gotify module
"""
import unittest
from unittest.mock import patch

from Alertify import gotify  # pylint: disable=import-error


class GotifyTest(unittest.TestCase):
    """
    Tests for methods in the Gotify class.
    """

    @classmethod
    def setUpClass(cls):
        cls.gotify_client = gotify.Gotify('http://localhost', '')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('requests.Session.request')
    def test_delete(self, mock_request):
        """Test"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.reason = 'OK'
        mock_request.return_value.content = ''

        self.assertDictEqual(
            self.gotify_client.delete('123'),
            {
                'status': 200,
                'reason': 'OK',
                'json': None,
            },
        )

    @patch('Alertify.gotify.Gotify.messages')
    def test_find_byfingerprint(self, mock_messages):
        """Test"""
        mock_messages.return_value = [
            {
                'id': 42,
                'extras': {'alertify': {'fingerprint': 'deadbeefcafebabe'}},
            }
        ]

        self.assertListEqual(
            self.gotify_client.find_byfingerprint({'fingerprint': 'deadbeefcafebabe'}),
            [42],
        )

    def test_messages(self):
        """Test"""
        self.assertDictEqual(
            self.gotify_client.messages(),
            dict(),
        )

    @patch('requests.Session.request')
    def test_send_alert_empty(self, mock_request):
        """Test"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.reason = 'OK'
        mock_request.return_value.content = ''

        self.assertDictEqual(
            self.gotify_client.send_alert(dict()),
            {
                'status': 200,
                'reason': 'OK',
                'json': None,
            },
        )

    @patch('requests.Session.request')
    def test_send_alert_dummy(self, mock_request):
        """Test"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.reason = 'OK'
        mock_request.return_value.content = ''

        self.assertDictEqual(
            self.gotify_client.send_alert(
                {
                    'title': 'TITLE',
                    'message': 'MESSAGE',
                    'priority': 0,
                    'extras': dict(),
                }
            ),
            {
                'status': 200,
                'reason': 'OK',
                'json': None,
            },
        )

    @patch('requests.Session.request')
    def test_healthcheck(self, mock_request):
        """Test"""
        mock_request.return_value.status_code = 200
        mock_request.return_value.reason = 'OK'
        mock_request.return_value.content = ''

        self.assertDictEqual(
            self.gotify_client.healthcheck(),
            {
                'status': 200,
                'reason': 'OK',
                'json': None,
            },
        )
