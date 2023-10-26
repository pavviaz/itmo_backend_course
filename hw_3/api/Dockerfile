FROM python:3.11

# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
# RUN apt-get install -y -q apt-utils python3-pip

WORKDIR /api

COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/