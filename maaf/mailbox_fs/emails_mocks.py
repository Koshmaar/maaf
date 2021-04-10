import copy
from typing import List
from datetime import datetime

from maaf.mailbox_fs.emails import Email, EmailServer, EmailID


class MockEmail(Email):
    def __init__(self, uid):
        self.uid = uid
        self.subject_ = ''
        self.date_ = None
        self.from_ = ''
        self.body_ = ''

    @property
    def subject(self) -> str:
        return self.subject_

    @property
    def from_email(self) -> str:
        return self.from_

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def body(self) -> str:
        return self.body_

    @property
    def headers(self) -> str:
        return ""


class MockEmailServer(EmailServer):
    def __init__(self, host: str, account: str, password: str, folder: str = ''):
        self.sample_email = MockEmail(1)
        with self.sample_email as m:
            m.subject_ = 'Import your mailbox and calendars'
            m.date_ = datetime(2021, 2, 13, 18, 3, 16)
            m.from_ = 'support@fastmail.com'
            m.body_ = 'Welcome! Let\'s get you up and running.\n\nHi there,\n\nThank you for signing up!'

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def logout(self):
        pass

    def get_sample_email(self) -> Email:
        return copy.copy(self.sample_email)

    def fetch_emails_headers(self) -> List[Email]:
        emails = []
        for i in range(4):
            em = self.get_sample_email()
            em.uid = i + 1
            emails.append(em)
        return emails

    def fetch_emails_bodies(self, email_uids: List[EmailID]) -> List[Email]:
        emails = []
        for uid in email_uids:
            em = self.get_sample_email()
            em.uid = uid
            emails.append(em)
        return emails
