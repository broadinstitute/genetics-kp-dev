# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class OperationFilterKgraphPercentileParameters(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, edge_attribute=None, threshold=95, remove_above_or_below='below', qedge_keys=None, qnode_keys=None):  # noqa: E501
        """OperationFilterKgraphPercentileParameters - a model defined in OpenAPI

        :param edge_attribute: The edge_attribute of this OperationFilterKgraphPercentileParameters.  # noqa: E501
        :type edge_attribute: str
        :param threshold: The threshold of this OperationFilterKgraphPercentileParameters.  # noqa: E501
        :type threshold: float
        :param remove_above_or_below: The remove_above_or_below of this OperationFilterKgraphPercentileParameters.  # noqa: E501
        :type remove_above_or_below: str
        :param qedge_keys: The qedge_keys of this OperationFilterKgraphPercentileParameters.  # noqa: E501
        :type qedge_keys: List[str]
        :param qnode_keys: The qnode_keys of this OperationFilterKgraphPercentileParameters.  # noqa: E501
        :type qnode_keys: List[str]
        """
        self.openapi_types = {
            'edge_attribute': str,
            'threshold': float,
            'remove_above_or_below': str,
            'qedge_keys': List[str],
            'qnode_keys': List[str]
        }

        self.attribute_map = {
            'edge_attribute': 'edge_attribute',
            'threshold': 'threshold',
            'remove_above_or_below': 'remove_above_or_below',
            'qedge_keys': 'qedge_keys',
            'qnode_keys': 'qnode_keys'
        }

        self._edge_attribute = edge_attribute
        self._threshold = threshold
        self._remove_above_or_below = remove_above_or_below
        self._qedge_keys = qedge_keys
        self._qnode_keys = qnode_keys

    @classmethod
    def from_dict(cls, dikt) -> 'OperationFilterKgraphPercentileParameters':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The OperationFilterKgraphPercentile_parameters of this OperationFilterKgraphPercentileParameters.  # noqa: E501
        :rtype: OperationFilterKgraphPercentileParameters
        """
        return util.deserialize_model(dikt, cls)

    @property
    def edge_attribute(self):
        """Gets the edge_attribute of this OperationFilterKgraphPercentileParameters.

        The name of the edge attribute to filter on.  # noqa: E501

        :return: The edge_attribute of this OperationFilterKgraphPercentileParameters.
        :rtype: str
        """
        return self._edge_attribute

    @edge_attribute.setter
    def edge_attribute(self, edge_attribute):
        """Sets the edge_attribute of this OperationFilterKgraphPercentileParameters.

        The name of the edge attribute to filter on.  # noqa: E501

        :param edge_attribute: The edge_attribute of this OperationFilterKgraphPercentileParameters.
        :type edge_attribute: str
        """
        if edge_attribute is None:
            raise ValueError("Invalid value for `edge_attribute`, must not be `None`")  # noqa: E501

        self._edge_attribute = edge_attribute

    @property
    def threshold(self):
        """Gets the threshold of this OperationFilterKgraphPercentileParameters.

        The percentile to threshold on.  # noqa: E501

        :return: The threshold of this OperationFilterKgraphPercentileParameters.
        :rtype: float
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Sets the threshold of this OperationFilterKgraphPercentileParameters.

        The percentile to threshold on.  # noqa: E501

        :param threshold: The threshold of this OperationFilterKgraphPercentileParameters.
        :type threshold: float
        """
        if threshold is not None and threshold > 100:  # noqa: E501
            raise ValueError("Invalid value for `threshold`, must be a value less than or equal to `100`")  # noqa: E501
        if threshold is not None and threshold < 0:  # noqa: E501
            raise ValueError("Invalid value for `threshold`, must be a value greater than or equal to `0`")  # noqa: E501

        self._threshold = threshold

    @property
    def remove_above_or_below(self):
        """Gets the remove_above_or_below of this OperationFilterKgraphPercentileParameters.

        Indicates whether to remove above or below the given threshold.  # noqa: E501

        :return: The remove_above_or_below of this OperationFilterKgraphPercentileParameters.
        :rtype: str
        """
        return self._remove_above_or_below

    @remove_above_or_below.setter
    def remove_above_or_below(self, remove_above_or_below):
        """Sets the remove_above_or_below of this OperationFilterKgraphPercentileParameters.

        Indicates whether to remove above or below the given threshold.  # noqa: E501

        :param remove_above_or_below: The remove_above_or_below of this OperationFilterKgraphPercentileParameters.
        :type remove_above_or_below: str
        """
        allowed_values = ["above", "below"]  # noqa: E501
        if remove_above_or_below not in allowed_values:
            raise ValueError(
                "Invalid value for `remove_above_or_below` ({0}), must be one of {1}"
                .format(remove_above_or_below, allowed_values)
            )

        self._remove_above_or_below = remove_above_or_below

    @property
    def qedge_keys(self):
        """Gets the qedge_keys of this OperationFilterKgraphPercentileParameters.

        This indicates if you only want to filter on specific edge_keys. If not provided or empty, all edges will be filtered on.  # noqa: E501

        :return: The qedge_keys of this OperationFilterKgraphPercentileParameters.
        :rtype: List[str]
        """
        return self._qedge_keys

    @qedge_keys.setter
    def qedge_keys(self, qedge_keys):
        """Sets the qedge_keys of this OperationFilterKgraphPercentileParameters.

        This indicates if you only want to filter on specific edge_keys. If not provided or empty, all edges will be filtered on.  # noqa: E501

        :param qedge_keys: The qedge_keys of this OperationFilterKgraphPercentileParameters.
        :type qedge_keys: List[str]
        """

        self._qedge_keys = qedge_keys

    @property
    def qnode_keys(self):
        """Gets the qnode_keys of this OperationFilterKgraphPercentileParameters.

        This indicates if you only want nodes corresponding to a specific list of qnode_keys to be removed. If not provided or empty, no nodes will be removed when filtering. Allows us to know what to do with the nodes connected to edges that are removed.  # noqa: E501

        :return: The qnode_keys of this OperationFilterKgraphPercentileParameters.
        :rtype: List[str]
        """
        return self._qnode_keys

    @qnode_keys.setter
    def qnode_keys(self, qnode_keys):
        """Sets the qnode_keys of this OperationFilterKgraphPercentileParameters.

        This indicates if you only want nodes corresponding to a specific list of qnode_keys to be removed. If not provided or empty, no nodes will be removed when filtering. Allows us to know what to do with the nodes connected to edges that are removed.  # noqa: E501

        :param qnode_keys: The qnode_keys of this OperationFilterKgraphPercentileParameters.
        :type qnode_keys: List[str]
        """

        self._qnode_keys = qnode_keys
