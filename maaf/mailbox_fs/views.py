from pathlib import Path
from datetime import datetime
from typing import List, DefaultDict
from collections import defaultdict

from maaf.mailbox_fs.filesystem import Filesystem
from maaf.mailbox_fs.emails import Email


class EmailView:
    def __init__(self, email: Email, folder: Path):
        self.uid = email.uid
        self.subject = email.subject
        self.filename_ = Path(email.from_email + "-" + self.subject)
        self.body = email.body + "\n\nHeaders:\n" + email.headers
        self.folder = folder
        self.ordinal = 1

    def __eq__(self, other):
        return self.uid == other.uid

    @property
    def filename(self) -> str:
        if self.ordinal > 1:
            return f"{self.filename_}-{self.ordinal}"
        else:
            return str(self.filename_)

    @filename.setter
    def filename(self, value: Path):
        self.filename_ = value


class FolderView:
    def __init__(self, top_level_path: Path, fs: Filesystem):
        self.top_level_path = top_level_path
        self.fs = fs
        self.fs.create_dir(self.top_level_path)
        self.folders: DefaultDict[Path, List[EmailView]] = defaultdict(
            list
        )  # key is "folder name"

    def add_email(self, email: Email):
        pass

    def remove_email(self, email: Email):
        pass

    def add_email_view(self, ev: EmailView):
        mail_views = self.folders[ev.folder]
        same_folder_cnt = len(mail_views)
        if same_folder_cnt == 0:
            self.fs.create_dir(self.top_level_path / ev.folder)
        elif same_folder_cnt >= 1:
            for v in mail_views:
                if v.filename == ev.filename:
                    ev.ordinal += 1
        mail_views.append(ev)
        self.write_email_view(ev)

    def remove_email_view(self, ev: EmailView):
        mail_views = self.folders[ev.folder]
        mail_views.remove(ev)
        self.fs.remove_file(self.top_level_path / ev.folder / ev.filename)
        if len(mail_views) == 0:
            self.fs.remove_dir(self.top_level_path / ev.folder)

    def write_email_view(self, ev: EmailView):
        # assumes folder already exists
        self.fs.write_file(self.top_level_path / ev.folder / ev.filename, ev.body)


class TimelineFolderView(FolderView):
    """
    Puts emails in <root>/timeline/{year}/{month}/{day}/ folders
    """

    def __init__(self, top_level_path: Path, fs: Filesystem):
        super().__init__(top_level_path / "timeline", fs)

    def add_email(self, email: Email):
        folder = str(datetime.strftime(email.date, '%Y/%m/%d'))
        ev = EmailView(email, Path(folder))
        self.add_email_view(ev)

    def remove_email(self, email: Email):
        folder = str(datetime.strftime(email.date, '%Y/%m/%d'))
        ev = EmailView(email, Path(folder))
        self.remove_email_view(ev)


class SenderFolderView(FolderView):
    """
    Puts emails in <root>/sender/{email}/ folders
    Filename consists only of topic, to not duplicate the sender email from main folder
    """

    def __init__(self, top_level_path: Path, fs: Filesystem):
        super().__init__(top_level_path / "sender", fs)

    def add_email(self, email: Email):
        folder = email.from_email
        ev = EmailView(email, Path(folder))
        ev.filename = email.subject
        self.add_email_view(ev)

    def remove_email(self, email: Email):
        folder = email.from_email
        ev = EmailView(email, Path(folder))
        ev.filename = email.subject
        self.remove_email_view(ev)
