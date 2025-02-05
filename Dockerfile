FROM docker.io/library/python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /bot

RUN apt-get update && apt-get install -y libffi-dev libnacl-dev python3-dev

COPY . .

RUN pip install -e .

WORKDIR /bot/boggart

CMD ["python3", "main.py"]