from http import HTTPStatus as Status


class ErrorResponse(object):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def to_dict(self):
        return self.__dict__


class CustomResponse:
    def __init__(self, code=Status.OK, message="", data=None):
        self.data = data
        self.code = code
        self.message = message

    def _get_data(self):
        data = dict(
            code=self.code,
            message=self.message
        )
        if self.data is not None:
            data.update({'data': self.data})
        return data

    def response(self):
        return self._get_data(), Status.OK

    def error(self):
        return ErrorResponse(message=self.message, code=Status.OK)
