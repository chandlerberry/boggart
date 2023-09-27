FROM python:3.10-slim

RUN apt update && apt install -y libffi-dev libnacl-dev python3-dev

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD python boggart.py -p "A renaissance portrait of a humanoid pig"