# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.log_entry import LogEntry
from openapi_server.models.message import Message
from openapi_server.models.schema2 import Schema2
from openapi_server import util

from openapi_server.models.log_entry import LogEntry  # noqa: E501
from openapi_server.models.message import Message  # noqa: E501
from openapi_server.models.schema2 import Schema2  # noqa: E501

class Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None, status=None, description=None, logs=None, workflow=None):  # noqa: E501
        """Response - a model defined in OpenAPI

        :param message: The message of this Response.  # noqa: E501
        :type message: Message
        :param status: The status of this Response.  # noqa: E501
        :type status: str
        :param description: The description of this Response.  # noqa: E501
        :type description: str
        :param logs: The logs of this Response.  # noqa: E501
        :type logs: List[LogEntry]
        :param workflow: The workflow of this Response.  # noqa: E501
        :type workflow: List[Schema2]
        """
        self.openapi_types = {
            'message': Message,
            'status': str,
            'description': str,
            'logs': List[LogEntry],
            'workflow': List[Schema2]
        }

        self.attribute_map = {
            'message': 'message',
            'status': 'status',
            'description': 'description',
            'logs': 'logs',
            'workflow': 'workflow'
        }

        self._message = message
        self._status = status
        self._description = description
        self._logs = logs
        self._workflow = workflow

    @classmethod
    def from_dict(cls, dikt) -> 'Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Response of this Response.  # noqa: E501
        :rtype: Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self):
        """Gets the message of this Response.


        :return: The message of this Response.
        :rtype: Message
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Response.


        :param message: The message of this Response.
        :type message: Message
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def status(self):
        """Gets the status of this Response.

        One of a standardized set of short codes, e.g. Success, QueryNotTraversable, KPsNotAvailable  # noqa: E501

        :return: The status of this Response.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Response.

        One of a standardized set of short codes, e.g. Success, QueryNotTraversable, KPsNotAvailable  # noqa: E501

        :param status: The status of this Response.
        :type status: str
        """

        self._status = status

    @property
    def description(self):
        """Gets the description of this Response.

        A brief human-readable description of the outcome  # noqa: E501

        :return: The description of this Response.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Response.

        A brief human-readable description of the outcome  # noqa: E501

        :param description: The description of this Response.
        :type description: str
        """

        self._description = description

    @property
    def logs(self):
        """Gets the logs of this Response.

        Log entries containing errors, warnings, debugging information, etc  # noqa: E501

        :return: The logs of this Response.
        :rtype: List[LogEntry]
        """
        return self._logs

    @logs.setter
    def logs(self, logs):
        """Sets the logs of this Response.

        Log entries containing errors, warnings, debugging information, etc  # noqa: E501

        :param logs: The logs of this Response.
        :type logs: List[LogEntry]
        """

        self._logs = logs

    @property
    def workflow(self):
        """Gets the workflow of this Response.


        :return: The workflow of this Response.
        :rtype: List[Schema2]
        """
        return self._workflow

    @workflow.setter
    def workflow(self, workflow):
        """Sets the workflow of this Response.


        :param workflow: The workflow of this Response.
        :type workflow: List[Schema2]
        """

        self._workflow = workflow
