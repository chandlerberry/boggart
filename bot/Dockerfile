FROM docker.io/library/python:3.11.8-slim-bookworm as builder

WORKDIR /build

RUN apt-get update && apt-get install -y libffi-dev libnacl-dev python3-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

ENV PYTHONUNBUFFERED=1

FROM docker.io/library/python:3.11.8-slim-bookworm

COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY boggart /bot

CMD ["python3", "/bot/main.py"]