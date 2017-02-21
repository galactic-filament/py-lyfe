FROM python

EXPOSE 80
ENV APP_PORT 80

# add app dir
ENV APP_DIR /srv/app
COPY ./app $APP_DIR
WORKDIR $APP_DIR

# add log dir
ENV APP_LOG_DIR $APP_DIR/log
VOLUME $APP_LOG_DIR

# installing deps
RUN pip install -r requirements.txt

CMD ["./bin/run-app"]
