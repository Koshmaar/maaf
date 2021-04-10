import os
from pathlib import Path


class Config:

    TOP_PATH = '/app/mails'
    HOST = ''
    ACCOUNT = ''
    PASSWORD = ''
    REFRESH_RATE = 30  # in seconds

    def __init__(self):
        self.TOP_PATH = os.environ.get('CONTAINER_MAILS_DIR', self.TOP_PATH)
        self.HOST = os.environ.get('HOST', self.HOST)
        self.ACCOUNT = os.environ.get('ACCOUNT', self.ACCOUNT)
        self.PASSWORD = os.environ.get('PASSWORD', self.PASSWORD)
        self.REFRESH_RATE = int(os.environ.get('REFRESH_RATE', self.REFRESH_RATE))
        self.MOCK = bool(os.environ.get('MOCK', False))

    @property
    def top_path(self) -> Path:
        return Path(self.TOP_PATH)
