FROM python:3.9

WORKDIR /home

COPY requirements.txt /home

RUN pip install -r requirements.txt

COPY . /home