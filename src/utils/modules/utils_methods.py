from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort

from ..constants import Constant


class UtilsMethods:

    @staticmethod
    def get_object_or_raise_404(model, params, filter_by=False, name="Object"):
        """
        :param model:
        :param params:
        :param filter_by:
        :param name:
        :return: model object or not found error
        """
        try:
            if filter_by:
                return model.query.filter_by(email=params).first()
            return model.query.get(params)
        except IntegrityError:
            abort(404, description=Constant.response.DOES_NOT_EXIST.format(object=name))

    @staticmethod
    def load_schema(schema, data):
        """
        Deserialize the object data through schema and run validations on form data.

        :param schema:
        :param data:
        :return: object
        """
        try:
            return schema.load(data)
        except ValidationError as err:
            abort(400, description=err.messages)


