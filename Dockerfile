FROM python

EXPOSE 80

COPY ./app /srv/app
WORKDIR /srv/app

RUN pip install -r requirements.txt

CMD ["./bin/run-app"]
