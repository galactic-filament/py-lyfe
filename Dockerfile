FROM python

COPY ./app /srv/app
WORKDIR /srv/app

RUN pip install -r requirements.txt

CMD ["python", "hello.py"]
