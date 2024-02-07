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

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x /app/deploy.sh && dos2unix /app/deploy.sh

EXPOSE 3000

ENTRYPOINT ["/bin/bash", "/app/deploy.sh"]

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]