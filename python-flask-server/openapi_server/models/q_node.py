# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class QNode(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, curie=None, type=None):  # noqa: E501
        """QNode - a model defined in OpenAPI

        :param id: The id of this QNode.  # noqa: E501
        :type id: str
        :param curie: The curie of this QNode.  # noqa: E501
        :type curie: object
        :param type: The type of this QNode.  # noqa: E501
        :type type: object
        """
        self.openapi_types = {
            'id': str,
            'curie': object,
            'type': object
        }

        self.attribute_map = {
            'id': 'id',
            'curie': 'curie',
            'type': 'type'
        }

        self._id = id
        self._curie = curie
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'QNode':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The QNode of this QNode.  # noqa: E501
        :rtype: QNode
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this QNode.

        QueryGraph internal identifier for this QNode. Recommended form: n00, n01, n02, etc.  # noqa: E501

        :return: The id of this QNode.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this QNode.

        QueryGraph internal identifier for this QNode. Recommended form: n00, n01, n02, etc.  # noqa: E501

        :param id: The id of this QNode.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def curie(self):
        """Gets the curie of this QNode.

        CURIE identifier for this node  # noqa: E501

        :return: The curie of this QNode.
        :rtype: object
        """
        return self._curie

    @curie.setter
    def curie(self, curie):
        """Sets the curie of this QNode.

        CURIE identifier for this node  # noqa: E501

        :param curie: The curie of this QNode.
        :type curie: object
        """

        self._curie = curie

    @property
    def type(self):
        """Gets the type of this QNode.


        :return: The type of this QNode.
        :rtype: object
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this QNode.


        :param type: The type of this QNode.
        :type type: object
        """

        self._type = type
