"""Custom response for all the data that provides common interface for all """
from http import HTTPStatus as Status


class CustomResponse:
    """Common response structure for all"""

    def __init__(self, code=Status.OK, message="", data=None):
        """Initial the class"""
        self.data = data
        self.code = code
        self.message = message

    def get_data(self):
        """Get the data in dict type"""
        data = dict(
            code=self.code,
            message=self.message
        )
        if self.data is not None:
            data.update({'data': self.data})
        return data

    def response(self):
        """Return response with the status code"""
        return self.get_data(), Status.OK
