FROM python:3.10-slim

RUN apt update && apt install -y libffi-dev libnacl-dev python3-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY boggart.py ./

CMD python boggart.py -p "A 3D render of the Docker whale logo"