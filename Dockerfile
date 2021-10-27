FROM python:3.8

WORKDIR /app

RUN apt-get update

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app


ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
