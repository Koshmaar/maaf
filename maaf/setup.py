from distutils.core import setup

setup(
    name='Mailbox as a Filesystem',
    version='0.0.1',
    author='Koshmaar',
    author_email='do.not@email.me',
    packages=['mailbox_fs'],
    install_requires=[
        'pathlib==1.0.1',
        'imap-tools==0.34.0'
    ]
)
