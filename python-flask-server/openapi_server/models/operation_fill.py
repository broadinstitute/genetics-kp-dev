# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
# from openapi_server.models.one_ofobjectobject import OneOfobjectobject
from openapi_server import util

# from openapi_server.models.one_ofobjectobject import OneOfobjectobject  # noqa: E501

class OperationFill(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, parameters=None):  # noqa: E501
        """OperationFill - a model defined in OpenAPI

        :param id: The id of this OperationFill.  # noqa: E501
        :type id: str
        :param parameters: The parameters of this OperationFill.  # noqa: E501
        :type parameters: OneOfobjectobject
        """
        self.openapi_types = {
            'id': str,
            'parameters': object
            # 'parameters': OneOfobjectobject
        }

        self.attribute_map = {
            'id': 'id',
            'parameters': 'parameters'
        }

        self._id = id
        self._parameters = parameters

    @classmethod
    def from_dict(cls, dikt) -> 'OperationFill':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The OperationFill of this OperationFill.  # noqa: E501
        :rtype: OperationFill
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this OperationFill.


        :return: The id of this OperationFill.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OperationFill.


        :param id: The id of this OperationFill.
        :type id: str
        """
        allowed_values = ["fill"]  # noqa: E501
        if id not in allowed_values:
            raise ValueError(
                "Invalid value for `id` ({0}), must be one of {1}"
                .format(id, allowed_values)
            )

        self._id = id

    @property
    def parameters(self):
        """Gets the parameters of this OperationFill.


        :return: The parameters of this OperationFill.
        :rtype: OneOfobjectobject
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this OperationFill.


        :param parameters: The parameters of this OperationFill.
        :type parameters: OneOfobjectobject
        """

        self._parameters = parameters
