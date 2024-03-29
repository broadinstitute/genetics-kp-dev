# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.message import Message
from openapi_server.models.query_log_level import QueryLogLevel
from openapi_server.models.query_workflow import QueryWorkflow
from openapi_server import util

from openapi_server.models.message import Message  # noqa: E501
from openapi_server.models.query_log_level import QueryLogLevel  # noqa: E501
from openapi_server.models.query_workflow import QueryWorkflow  # noqa: E501

class Query(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, message=None, log_level=None, workflow=None, submitter=None):  # noqa: E501
        """Query - a model defined in OpenAPI

        :param message: The message of this Query.  # noqa: E501
        :type message: Message
        :param log_level: The log_level of this Query.  # noqa: E501
        :type log_level: QueryLogLevel
        :param workflow: The workflow of this Query.  # noqa: E501
        :type workflow: QueryWorkflow
        :param submitter: The submitter of this Query.  # noqa: E501
        :type submitter: str
        """
        self.openapi_types = {
            'message': Message,
            'log_level': QueryLogLevel,
            'workflow': QueryWorkflow,
            'submitter': str
        }

        self.attribute_map = {
            'message': 'message',
            'log_level': 'log_level',
            'workflow': 'workflow',
            'submitter': 'submitter'
        }

        self._message = message
        self._log_level = log_level
        self._workflow = workflow
        self._submitter = submitter

    @classmethod
    def from_dict(cls, dikt) -> 'Query':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Query of this Query.  # noqa: E501
        :rtype: Query
        """
        return util.deserialize_model(dikt, cls)

    @property
    def message(self):
        """Gets the message of this Query.


        :return: The message of this Query.
        :rtype: Message
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Query.


        :param message: The message of this Query.
        :type message: Message
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def log_level(self):
        """Gets the log_level of this Query.


        :return: The log_level of this Query.
        :rtype: QueryLogLevel
        """
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        """Sets the log_level of this Query.


        :param log_level: The log_level of this Query.
        :type log_level: QueryLogLevel
        """

        self._log_level = log_level

    @property
    def workflow(self):
        """Gets the workflow of this Query.


        :return: The workflow of this Query.
        :rtype: QueryWorkflow
        """
        return self._workflow

    @workflow.setter
    def workflow(self, workflow):
        """Sets the workflow of this Query.


        :param workflow: The workflow of this Query.
        :type workflow: QueryWorkflow
        """

        self._workflow = workflow

    @property
    def submitter(self):
        """Gets the submitter of this Query.

        Any string for self-identifying the submitter of a query. The purpose of this optional field is to aid in the tracking of the source of queries for development and issue resolution.  # noqa: E501

        :return: The submitter of this Query.
        :rtype: str
        """
        return self._submitter

    @submitter.setter
    def submitter(self, submitter):
        """Sets the submitter of this Query.

        Any string for self-identifying the submitter of a query. The purpose of this optional field is to aid in the tracking of the source of queries for development and issue resolution.  # noqa: E501

        :param submitter: The submitter of this Query.
        :type submitter: str
        """

        self._submitter = submitter
