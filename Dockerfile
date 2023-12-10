FROM python:3.11.6-slim-bookworm

RUN apt update && apt install -y libffi-dev libnacl-dev python3-dev

WORKDIR /usr/src/app
COPY config /config

RUN pip install --no-cache-dir -r requirements.txt

CMD python boggart.py