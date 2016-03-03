from flask.ext.api import status
from flask import json


def request_json(client, method, url, body=None):
    request = getattr(client, method)
    response = request(url, data=json.dumps(body),
                       content_type='application/json')
    assert status.is_success(response.status_code)
    response_body = json.loads(response.get_data(as_text=True))
    return response_body


def create_post(client, body):
    response_body = request_json(client, 'post', '/posts', body)
    assert type(response_body['id']) is int

    return response_body
