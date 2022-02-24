FROM python:3.7-alpine as build-env

# alpine deps install
RUN apk add --virtual native-deps \
  curl gcc g++ libffi-dev postgresql-dev

# add app dir
ENV APP_DIR /srv/app
COPY ./app $APP_DIR
WORKDIR $APP_DIR

# poetry and deps
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH /root/.poetry/bin:$PATH
RUN poetry config virtualenvs.in-project true \
    && poetry install
ENV PATH $APP_DIR/.venv/bin:$PATH

# alpine deps cleanup
RUN apk del native-deps


FROM python:3.7-alpine as runtime-env

# alpine deps install
RUN apk add --virtual native-deps \
  postgresql-dev

# app port
EXPOSE 80
ENV APP_PORT 80

# importing from build-env
COPY --from=build-env /srv/app /srv/app
WORKDIR /srv/app

CMD ["./bin/run-app.sh"]
