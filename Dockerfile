FROM python

RUN apt-get update -q \
  && apt-get install -yq netcat

EXPOSE 80

COPY ./app /srv/app
WORKDIR /srv/app

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
