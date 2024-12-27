FROM python:3.13.1-alpine3.21
WORKDIR /python

COPY requirements.txt /python/build/requirements.txt 
RUN pip3 install --upgrade pip
RUN pip3 install -r build/requirements.txt
