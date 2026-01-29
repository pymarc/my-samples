FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y \
    software-properties-common \
    ca-certificates \
    curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.13 \
    python3.13-venv \
    python3.13-distutils \
    && rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.13
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13

COPY . /app/

RUN python3.13 -m pip install --no-cache-dir -r requirements.txt

CMD ["python3.13", "fetch.py", "-u", "https://8.8.8.8", "https://onet.pl", "https://mbank.pl", "-c", "5"]
