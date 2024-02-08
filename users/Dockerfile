# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y dos2unix && \
    pip install pipenv && \
    pipenv install --system --deploy

COPY wait-for-it.sh wait-for-it.sh
RUN dos2unix wait-for-it.sh && \
    chmod +x wait-for-it.sh

EXPOSE 3000

LABEL author="h.maury@uniandes.edu.co"

# CMD ["./wait-for-it.sh", "user_db:5432", "-t", "600", "--", "FLASK_APP=./src/main.py",  "flask", "run", "--port=3000", "--host=0.0.0.0"]

CMD ["/bin/sh", "-c", "/app/wait-for-it.sh user_db:5432 -t 600 -- && export FLASK_APP=./src/main.py && flask run --port=3000 --host=0.0.0.0"]

