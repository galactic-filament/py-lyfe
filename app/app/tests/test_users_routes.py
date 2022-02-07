import json
from unittest.mock import patch

from requests import codes
import bcrypt

mock_create_user_body = {"username": "username", "password": "password"}
mock_user_id = 1


def test_create_user(mock_client):
    with patch("blueprints.users.db.session.add") as mock_add, patch(
        "blueprints.users.db.session.commit"
    ) as mock_commit:

        def mock_add_side_effect(user):
            user.id = mock_user_id

        mock_add.side_effect = mock_add_side_effect
        mock_commit.return_value = None

        response = mock_client.post(
            "/users",
            data=json.dumps(mock_create_user_body),
            content_type="application/json",
        )
        assert response.status_code == codes.created

        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"] == mock_user_id
        assert bcrypt.checkpw(
            mock_create_user_body["password"].encode(),
            response_body["hashed_password"].encode(),
        )
