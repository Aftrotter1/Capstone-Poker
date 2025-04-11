
# Stage 1: Base build stage
FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /Capstone_Poker_Django

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt
COPY . .

CMD python manage.py runserver 0.0.0.0:8000


