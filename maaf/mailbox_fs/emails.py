from typing import List
from dataclasses import dataclass
from datetime import datetime
from imap_tools import MailBox, MailMessage

EmailID = int


@dataclass
class Email:
    uid: EmailID
    msg: MailMessage

    @property
    def subject(self) -> str:
        return self.msg.subject

    @property
    def from_email(self) -> str:
        return self.msg.from_

    @property
    def date(self) -> datetime:
        return self.msg.date

    @property
    def body(self) -> str:
        return self.msg.text

    @property
    def headers(self) -> str:
        hds = [f"{k}:{v}" for k, v in self.msg.headers.items()]
        return "\n".join(hds)

    def __str__(self):
        if len(self.body) > 510:
            excerpt = f"<{self.body[:250]} ... {self.body[-250:]}>"
        else:
            excerpt = f"<{self.body}>"
        excerpt = excerpt.replace('\n', '')
        return f"{self.uid} - {self.subject} - {self.date} - \nbody: {excerpt}"

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class EmailServer:
    def __init__(self, host: str, account: str, password: str, folder: str = '/'):
        """
        :param folder: name of folder prepended with /, ie. '/foobar'
        """
        assert '/' in folder
        print(f"Connecting to {account} at {host}...")
        self.server = MailBox(host)
        self.server.login(account, password, initial_folder='INBOX' + folder)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def logout(self):
        self.server.logout()

    def fetch_emails_headers(self) -> List[Email]:
        """
        :return: all emails headers on server
        """
        results: List[Email] = []
        for msg in self.server.fetch(criteria='ALL', headers_only=True):
            email = Email(int(msg.uid), msg)
            results.append(email)
        return results

    def fetch_emails_bodies(self, email_uids: List[EmailID]) -> List[Email]:
        """
        :return: full emails from the email_uids list
        """
        if len(email_uids) == 0:
            return []
        results: List[Email] = []
        uids = 'UID ' + ",".join(map(str, email_uids))

        for msg in self.server.fetch(criteria=uids):
            email = Email(int(msg.uid), msg)
            results.append(email)
        return results
