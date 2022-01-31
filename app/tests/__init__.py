import logging
from unittest.mock import MagicMock

from flask import json
from requests import codes

from app import create_app


def request_json(client, method, url, body=None, status=codes.ok):
    request = getattr(client, method)
    response = request(url, data=json.dumps(body), content_type="application/json")
    assert response.status_code == status
    response_body = json.loads(response.get_data(as_text=True))
    return response_body


def create_post(client, body):
    response_body = request_json(client, "post", "/posts", body, codes.created)
    assert type(response_body["id"]) is int

    return response_body


class MockDao:
    def __init__(self, _db):
        pass

    def init_app(self, _app):
        pass

    def add(self, _record):
        pass

    def delete(self, _record):
        pass


def create_test_app():
    class MockFileHandler:
        level = logging.INFO

        def setFormatter(self, _formatter):
            pass

        def handle(self, _record):
            pass

    logging.FileHandler = MagicMock(return_value=MockFileHandler())

    app = create_app("", MockDao(None), "")
    app.debug = True

    return app
