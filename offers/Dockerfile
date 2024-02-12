# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /usr/src/offer

COPY . .

COPY Pipfile Pipfile.lock ./

# RUN python -m pip install --upgrade pip
# RUN pip install pipenv && pipenv install --dev --system --deploy

RUN apt-get update && \
    apt-get install -y dos2unix && \
    pip install pipenv && \
    pipenv install --system --deploy

# ENV FLASK_APP=src.main
# COPY wait-for-it.sh wait-for-it.sh
# RUN chmod +x wait-for-it.sh

LABEL author="f.alarconf@uniandes.edu.co"

# CMD ["./wait-for-it.sh", "offer_db:5432", "-t", "600", "--", "flask", "run", "--port=3003", "--host=0.0.0.0"]

CMD ["/bin/sh", "-c", "export FLASK_APP=./src/main.py && flask run --port=3003 --host=0.0.0.0"]