# An image for the web image checker API
FROM python:3.13

RUN mkdir /app
WORKDIR /app

RUN pip install uv

COPY ./samples/web_images_checker /app/

RUN uv pip install --system .

ENV PYTHONPATH=/app