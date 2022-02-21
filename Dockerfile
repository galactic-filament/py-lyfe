FROM python

# app port
EXPOSE 80
ENV APP_PORT 80

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

CMD ["./bin/run-app"]
