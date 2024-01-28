# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /usr/src/offer

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

# Add wait-for-it
COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh

EXPOSE 3003

LABEL author="f.alarconf@uniandes.edu.co"

CMD ["./wait-for-it.sh", "offer_db:5432", "-t", "600", "--", "flask", "run", "--port=3003", "--host=0.0.0.0"]
