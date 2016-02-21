FROM python

EXPOSE 80

RUN apt-get update -q \
  && apt-get install -yq netcat

COPY ./app /srv/app
WORKDIR /srv/app

RUN pip install -r requirements.txt

CMD ["python", "./run.py"]
