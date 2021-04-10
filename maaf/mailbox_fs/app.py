from typing import List, Tuple, Dict

from maaf.mailbox_fs.config import Config
from maaf.mailbox_fs.emails import EmailServer, Email, EmailID
from maaf.mailbox_fs.filesystem import Filesystem
from maaf.mailbox_fs.views import TimelineFolderView, SenderFolderView


class App:
    def __init__(self, cfg: Config, server: EmailServer, fs: Filesystem):
        self.cfg = cfg
        self.server = server
        self.fs = fs
        self.emails: Dict[EmailID, Email] = {}

        self.fs.create_dir(cfg.top_path)
        self.views = [
            TimelineFolderView(cfg.top_path, self.fs),
            SenderFolderView(cfg.top_path, self.fs),
        ]

    def __del__(self):
        self.fs.remove_dir(self.cfg.top_path)

    def refresh(self):
        """
        for new mail: create Views, which renders mail to every needed point of fs
        for old mails that were removed: remove views, which remove their folders and files from fs
        """
        print("-----\nRefreshing...")

        fetched_email_headers: List[Email] = self.server.fetch_emails_headers()
        [new_emails_uids, removed_emails_uids] = self.diff_emails_list_with_local(fetched_email_headers)

        for uid in removed_emails_uids:
            print(f"\nRemoving email: \n {self.emails[uid]}")
            for v in self.views:
                v.remove_email(self.emails[uid])
            del self.emails[uid]

        # fetch full bodies of emails that aren't yet in memory
        fetched_email_bodies: List[Email] = self.server.fetch_emails_bodies(
            new_emails_uids
        )

        for m in fetched_email_bodies:
            print(f"\nReceived new email:\n {m}")
            for v in self.views:
                v.add_email(m)
            self.emails[m.uid] = m

    def diff_emails_list_with_local(self, fetched_email_headers: List[Email]) -> Tuple[List[EmailID], List[EmailID]]:

        new_emails_uids: List[EmailID] = []
        removed_emails_uids: List[EmailID] = []

        for mh in fetched_email_headers:
            if self.emails.get(mh.uid) is None:
                new_emails_uids.append(mh.uid)

        for m_uid in self.emails.keys():
            if not any(x for x in fetched_email_headers if x.uid == m_uid):
                removed_emails_uids.append(m_uid)

        return new_emails_uids, removed_emails_uids
