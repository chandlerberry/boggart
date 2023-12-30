FROM python:3.11.6-bookworm

RUN apt update && apt install -y libffi-dev libnacl-dev python3-dev

WORKDIR /usr/src/app
COPY . .

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/usr/local/bin/python3", "/usr/src/app/boggart.py"]