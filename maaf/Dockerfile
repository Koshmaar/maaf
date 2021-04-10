FROM python:3.8-slim-buster

WORKDIR /app

COPY setup.py ./maaf/
COPY mailbox_fs/ ./maaf/mailbox_fs/
RUN pip install ./maaf/

CMD ["python", "-m", "mailbox_fs.main"]
