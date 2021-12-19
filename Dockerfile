FROM python:3.9-slim


RUN mkdir -p /app/
WORKDIR /app/

COPY . /app/

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 5000

CMD [ "./run.sh" ]