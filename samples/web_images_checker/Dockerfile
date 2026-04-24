# An image for the web image checker API
FROM python:3.13

RUN mkdir /app
WORKDIR /app

RUN pip install uv

COPY . /app

RUN uv pip install --system .