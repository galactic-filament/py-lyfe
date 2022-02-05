import logging
from unittest.mock import patch

from app import create_app


def create_test_app():
    with patch("app.FileHandler") as mock_file_handler:

        class MockFileHandler:
            level = logging.INFO

            def setFormatter(self, formatter):
                pass

            def handle(self, record):
                pass

        mock_file_handler.return_value = MockFileHandler()

        app = create_app("", "")
        app.debug = True

        return app
