FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv && \
  apt-get update && \
  apt-get install -y libpq-dev gcc && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
  apt-get install -y dos2unix

RUN pip install pipenv psycopg2

COPY Pipfile Pipfile.lock ./

RUN pipenv install

COPY . .

RUN chmod +x /app/deploy.sh && dos2unix /app/deploy.sh

ENTRYPOINT ["/bin/bash", "/app/deploy.sh"]