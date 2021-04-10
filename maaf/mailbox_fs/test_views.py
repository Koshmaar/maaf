import unittest
from unittest.mock import Mock
from pathlib import Path

from maaf.mailbox_fs.filesystem import MockFilesystem
from maaf.mailbox_fs.emails_mocks import MockEmailServer
from maaf.mailbox_fs.views import SenderFolderView, TimelineFolderView


class TestViews(unittest.TestCase):
    def setUp(self) -> None:
        print("")
        self.fs = MockFilesystem()
        self.fs.write_file = Mock()
        self.fs.remove_file = Mock()
        self.fs.create_dir = Mock()
        self.fs.remove_dir = Mock()
        self.server = MockEmailServer('', '', '', '')
        self.tfv = TimelineFolderView(Path("/"), self.fs)
        self.sfv = SenderFolderView(Path("/"), self.fs)
        self.sample_subject = self.server.get_sample_email().subject

    def test_timelinefolder(self):
        self.tfv.add_email(self.server.get_sample_email())
        self.assertEqual(self.fs.write_file.call_count, 1)
        call = self.fs.write_file.call_args_list[0][0]
        self.assertEqual(
            str(call[0]),
            '/timeline/2021/02/13/support@fastmail.com-' + self.sample_subject,
        )
        self.assertEqual(self.fs.create_dir.call_count, 3)

    def test_senderfolder(self):
        self.sfv.add_email(self.server.get_sample_email())
        self.assertEqual(self.fs.write_file.call_count, 1)
        call = self.fs.write_file.call_args_list[0][0]
        self.assertEqual(
            str(call[0]), '/sender/support@fastmail.com/' + self.sample_subject
        )

    def test_filename_duplication(self):
        mail = self.server.get_sample_email()
        self.sfv.add_email(mail)
        self.assertEqual(self.fs.write_file.call_count, 1)
        call = self.fs.write_file.call_args_list[0][0]
        self.assertEqual(
            str(call[0]), '/sender/support@fastmail.com/' + self.sample_subject
        )

        mail.uid = 2
        self.sfv.add_email(mail)
        self.assertEqual(self.fs.write_file.call_count, 2)
        call = self.fs.write_file.call_args_list[1][0]
        self.assertEqual(
            str(call[0]), '/sender/support@fastmail.com/' + self.sample_subject + '-2'
        )

        mail.uid = 3
        self.sfv.add_email(mail)
        self.assertEqual(self.fs.write_file.call_count, 3)
        call = self.fs.write_file.call_args_list[2][0]
        self.assertEqual(
            str(call[0]), '/sender/support@fastmail.com/' + self.sample_subject + '-3'
        )

    def test_email_deletion(self):
        mail = self.server.get_sample_email()
        self.sfv.add_email(mail)
        self.assertEqual(self.fs.write_file.call_count, 1)
        call = self.fs.write_file.call_args_list[0][0]
        self.assertEqual(
            str(call[0]), '/sender/support@fastmail.com/' + self.sample_subject
        )

        self.sfv.remove_email(mail)
        self.assertEqual(self.fs.remove_file.call_count, 1)
        call = self.fs.remove_file.call_args_list[0][0]
        self.assertEqual(
            str(call[0]), '/sender/support@fastmail.com/' + self.sample_subject
        )
        self.assertEqual(self.fs.remove_dir.call_count, 1)
