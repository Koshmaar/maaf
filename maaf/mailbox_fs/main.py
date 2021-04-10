import time
import imaplib

from maaf.mailbox_fs.app import App
from maaf.mailbox_fs.config import Config
from maaf.mailbox_fs.emails import EmailServer
from maaf.mailbox_fs.emails_mocks import MockEmailServer
from maaf.mailbox_fs.filesystem import Filesystem, MockFilesystem


if __name__ == '__main__':
    print("Starting Mailbox As A Filesystem 0.0.1")
    config = Config()

    server_class = EmailServer
    fs_class = Filesystem

    if config.MOCK:
        print("Warning: using mocks")
        server_class = MockEmailServer
        fs_class = MockFilesystem

    try:
        server = server_class(config.HOST, config.ACCOUNT, config.PASSWORD)
        app = App(config, server, fs_class())
        while True:
            app.refresh()
            time.sleep(config.REFRESH_RATE)
    except KeyboardInterrupt:
        pass
    except (imaplib.IMAP4.error, OSError) as exc:
        print(exc)
