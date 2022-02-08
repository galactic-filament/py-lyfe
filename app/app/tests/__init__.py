import logging
from unittest.mock import patch

from util import create_app


def create_test_app(db_uri=""):
    with patch("util.FileHandler") as mock_file_handler:

        class MockFileHandler:
            level = logging.INFO

            def setFormatter(self, formatter):
                pass

            def handle(self, record):
                pass

        mock_file_handler.return_value = MockFileHandler()

        app = create_app(db_uri, "")
        app.debug = True

        return app
