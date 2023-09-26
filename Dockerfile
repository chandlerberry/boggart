FROM python:3.10-slim

# TODO: environment variable to set for path to keys.json (bind mount)

RUN apt update && apt install -y libffi-dev libnacl-dev python3-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY boggart.py ./

CMD python boggart.py