# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /usr/src/user

COPY . .

RUN pip install --user pipenv 

RUN pipenv shell

RUN pipenv install  

COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh

EXPOSE 3000

LABEL author="h.maury@uniandes.edu.co"

CMD ["./wait-for-it.sh", "user_db:5432", "-t", "600", "--", "FLASK_APP=./src/main.py",  "flask", "run", "--port=3000", "--host=0.0.0.0"]
