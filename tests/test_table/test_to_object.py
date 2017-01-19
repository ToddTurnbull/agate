#!/usr/bin/env python
# -*- coding: utf8 -*-

from collections import OrderedDict

from agate import Table
from agate.testcase import AgateTestCase
from agate.data_types import *


class TestObject(AgateTestCase):
    def setUp(self):
        self.rows = (
            (1, 'a', True, '11/4/2015', '11/4/2015 12:22 PM', '4:15'),
            (2, u'👍', False, '11/5/2015', '11/4/2015 12:45 PM', '6:18'),
            (None, 'b', None, None, None, None)
        )

        self.column_names = (
            'number', 'text', 'boolean', 'date', 'datetime', 'timedelta'
        )

        self.column_types = (
            Number(), Text(), Boolean(), Date(), DateTime(), TimeDelta()
        )

    def test_to_object(self):
        table1 = Table(self.rows, self.column_names, self.column_types)

        obj = table1.to_object()
        table2 = Table.from_object(obj)

        self.assertColumnNames(table2, table1.column_names)
        self.assertColumnTypes(table2, (Number, Text, Boolean, Date, DateTime, TimeDelta))
        self.assertRows(table2, table1.rows)

    def test_to_object_key(self):
        table = Table(self.rows, self.column_names, self.column_types)

        obj = table.to_object('text')

        self.assertEqual(table.columns['text'].values(), tuple(obj.keys()))

        rows = obj.values()
        for i, row in enumerate(rows):
            self.assertEqual(table.rows[i].dict(), row)

    def test_to_object_func(self):
        table = Table(self.rows, self.column_names, self.column_types)

        key_func = lambda row: row['text']
        obj = table.to_object(key_func)

        self.assertEqual([key_func(row) for row in table.rows], list(obj.keys()))

        rows = obj.values()
        for i, row in enumerate(rows):
            self.assertEqual(table.rows[i].dict(), row)

