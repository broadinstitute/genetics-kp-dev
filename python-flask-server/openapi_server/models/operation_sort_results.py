# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.operation_annotate_runner_parameters import OperationAnnotateRunnerParameters
from openapi_server import util

from openapi_server.models.operation_annotate_runner_parameters import OperationAnnotateRunnerParameters  # noqa: E501

class OperationSortResults(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, parameters=None, runner_parameters=None):  # noqa: E501
        """OperationSortResults - a model defined in OpenAPI

        :param id: The id of this OperationSortResults.  # noqa: E501
        :type id: str
        :param parameters: The parameters of this OperationSortResults.  # noqa: E501
        :type parameters: object
        :param runner_parameters: The runner_parameters of this OperationSortResults.  # noqa: E501
        :type runner_parameters: OperationAnnotateRunnerParameters
        """
        self.openapi_types = {
            'id': str,
            'parameters': object,
            'runner_parameters': OperationAnnotateRunnerParameters
        }

        self.attribute_map = {
            'id': 'id',
            'parameters': 'parameters',
            'runner_parameters': 'runner_parameters'
        }

        self._id = id
        self._parameters = parameters
        self._runner_parameters = runner_parameters

    @classmethod
    def from_dict(cls, dikt) -> 'OperationSortResults':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The OperationSortResults of this OperationSortResults.  # noqa: E501
        :rtype: OperationSortResults
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this OperationSortResults.


        :return: The id of this OperationSortResults.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OperationSortResults.


        :param id: The id of this OperationSortResults.
        :type id: str
        """
        allowed_values = ["sort_results"]  # noqa: E501
        if id not in allowed_values:
            raise ValueError(
                "Invalid value for `id` ({0}), must be one of {1}"
                .format(id, allowed_values)
            )

        self._id = id

    @property
    def parameters(self):
        """Gets the parameters of this OperationSortResults.


        :return: The parameters of this OperationSortResults.
        :rtype: object
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this OperationSortResults.


        :param parameters: The parameters of this OperationSortResults.
        :type parameters: object
        """

        self._parameters = parameters

    @property
    def runner_parameters(self):
        """Gets the runner_parameters of this OperationSortResults.


        :return: The runner_parameters of this OperationSortResults.
        :rtype: OperationAnnotateRunnerParameters
        """
        return self._runner_parameters

    @runner_parameters.setter
    def runner_parameters(self, runner_parameters):
        """Sets the runner_parameters of this OperationSortResults.


        :param runner_parameters: The runner_parameters of this OperationSortResults.
        :type runner_parameters: OperationAnnotateRunnerParameters
        """

        self._runner_parameters = runner_parameters
