#!/usr/bin/env python
# pylint: disable=W0212

from collections import OrderedDict

import six


def to_object(self, key=None):
    """
    Convert this table to a Python object. By default this will be a list
    containing an OrderedDict for each row. If the :code:`key` parameter is
    specified, this will be an OrderedDict.

    :param key:
        If specified, may be either the name of a column from this table
        containing unique values or a :class:`function` that takes a row and
        returns a unique value.
    """
    # Keyed
    if key is not None:
        key_is_row_function = hasattr(key, '__call__')

        output = OrderedDict()

        for row in self._rows:
            if key_is_row_function:
                k = key(row)
            else:
                k = row[key]

            if k in output:
                raise ValueError('Value %s is not unique in the key column.' % six.text_type(k))

            values = tuple(row)

            output[k] = OrderedDict(zip(row.keys(), values))

        return output
    # Default
    else:
        output = []

        for row in self._rows:
            values = tuple(row)
            output.append(OrderedDict(zip(row.keys(), values)))

        return output

