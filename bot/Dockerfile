FROM docker.io/library/python:3.11.8-slim-bookworm@sha256:93f65e226cd297cee60fbdc2241d2415a479cb68d0199da4345ec8d2627c9bbf as builder

WORKDIR /build

RUN apt-get update && apt-get install -y libffi-dev libnacl-dev python3-dev

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

ENV PYTHONUNBUFFERED=1

FROM docker.io/library/python:3.11.8-slim-bookworm@sha256:93f65e226cd297cee60fbdc2241d2415a479cb68d0199da4345ec8d2627c9bbf

COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY src /bot/src

CMD ["python3", "/bot/src/boggart.py"]