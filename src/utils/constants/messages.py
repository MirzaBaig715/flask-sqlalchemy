"""This is where we will add all the response that will be sent from server"""


class ResponseMessages:
    """Response messages in string format"""

    OPERATION_SUCCESS = "{object} {operation} successfully"
    DOES_NOT_EXIST = "{object} not found"
    EMAIL_ALREADY_IN_USE = "Email address is already in use"
    NO_INPUT_DATA = "No data provided"
    INCORRECT_USER = "Email or password is incorrect"
