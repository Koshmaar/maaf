import unittest
from datetime import datetime, timezone

from maaf.mailbox_fs.config import Config
from maaf.mailbox_fs.emails import EmailServer, Email
from maaf.mailbox_fs.emails_mocks import MockEmailServer


class TestEmailServer(unittest.TestCase):
    """
    Connects to test inbox which contains specific emails
    """

    def setUp(self):
        server_class = EmailServer
        config = Config()
        if config.MOCK:
            print("Warning: using mocks")
            server_class = MockEmailServer
        self.server = server_class(config.HOST, config.ACCOUNT, config.PASSWORD, '/units')

    def tearDown(self):
        self.server.logout()

    def test_fetch_headers(self):
        emails = self.server.fetch_emails_headers()
        self.assertEqual(len(emails), 4)

        m: Email = emails[0]
        self.assertEqual(m.uid, 1)
        self.assertEqual(m.subject, 'Import your mailbox and calendars')
        self.assertEqual(
            m.date.astimezone(timezone.utc),
            datetime(2021, 2, 13, 17, 3, 16, tzinfo=timezone.utc),
        )
        self.assertEqual(m.from_email, 'support@fastmail.com')

    def test_fetch_body(self):
        emails = self.server.fetch_emails_bodies([1, 2, 4])
        self.assertEqual(len(emails), 3)

        m: Email = emails[0]
        self.assertEqual(m.uid, 1)
        self.assertEqual(m.subject, 'Import your mailbox and calendars')
        self.assertEqual(
            m.date.astimezone(timezone.utc),
            datetime(2021, 2, 13, 17, 3, 16, tzinfo=timezone.utc),
        )
        self.assertEqual(m.from_email, 'support@fastmail.com')
        self.assertIn('Welcome! Let\'s get you up and running', m.body)

    def test_fetch_bodies_empty_list(self):
        emails = self.server.fetch_emails_bodies([])
        self.assertEqual(len(emails), 0)
