# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module: error_handlers
"""
from flask import jsonify
from service.models import DataValidationError
from service import app
from . import status
import unittest

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data"""
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad requests with 400_BAD_REQUEST"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """Handles unsupported HTTP methods with 405_METHOD_NOT_SUPPORTED"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Handles unexpected server error with 500_SERVER_ERROR"""
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_request_validation_error(self):
        # Test handling DataValidationError
        with app.app_context():
            error = DataValidationError("Test validation error")
            response = request_validation_error(error)
            self.assertEqual(response[1], HTTP_400_BAD_REQUEST)
            self.assertIn(b"Bad Request", response[0].data)
            self.assertIn(b"Test validation error", response[0].data)

    def test_bad_request(self):
        # Test handling bad request
        error_message = "Test bad request error"
        response = bad_request(ValueError(error_message))
        self.assertEqual(response[1], HTTP_400_BAD_REQUEST)
        self.assertIn(b"Bad Request", response[0].data)
        self.assertIn(error_message.encode(), response[0].data)


        
    # Add similar test methods for other error handlers (not_found, method_not_supported, mediatype_not_supported, internal_server_error)

if __name__ == "__main__":
    unittest.main()