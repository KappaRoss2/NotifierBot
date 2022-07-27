FROM python:latest
WORKDIR usr/src/bot
COPY requirements.txt /usr/src/bot
RUN pip install -r requirements.txt