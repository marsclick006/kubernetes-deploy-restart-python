FROM python:3.9-slim

ENV USERNAME USERNAME
ENV PASSWORD PASSWORD

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD python ./web-server.py
