FROM python:3.9

WORKDIR /home

RUN pip install pipenv

COPY Pipfile /home

COPY Pipfile.lock /home

RUN pipenv install --system --deploy

COPY . /home