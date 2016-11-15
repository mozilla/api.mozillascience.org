FROM python:3.5

WORKDIR /app
EXPOSE 7001
COPY ./requirements.txt .
RUN pip install -r requirements.txt ipdb==0.9.3 --no-cache-dir --disable-pip-version-check
RUN apt-get update && apt-get install -y graphviz
COPY ./app .
