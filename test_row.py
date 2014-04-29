# coding: utf-8

import datetime
import unittest

from textwrap import dedent

from row import parse, parse_file


class TestTab(unittest.TestCase):
    def test_raise_exception_if_field_names_and_types_are_not_present(self):
        contents = dedent('''
        only\tfield\tnames
        ''').strip()
        with self.assertRaises(ValueError):
            parse(contents)

        contents = dedent('''
        field\tnames
        wrong\ttypes
        ''').strip()
        with self.assertRaises(ValueError):
            parse(contents)

    def test_no_records(self):
        contents = dedent('''
        a\tb\tc\td\te
        int\tint\tint\tint\tint
        ''').strip()
        expected = []
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_normal_records(self):
        contents = dedent('''
        a\tb\tc\td\te
        int\tint\tint\tint\tint
        123\t456\t789\t0\t-1
        -1\t0\t789\t456\t123
        ''').strip()
        expected = [
            {'a': 123, 'b': 456, 'c': 789, 'd': 0,   'e': -1},
            {'a': -1,  'b': 0,   'c': 789, 'd': 456, 'e': 123},
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_empty_lines_should_be_ignored(self):
        contents = dedent('''
        a\tb\tc\td\te
        int\tint\tint\tint\tint
        123\t456\t789\t0\t-1


        -1\t0\t789\t456\t123
        ''').strip() + '\n'
        expected = [
            {'a': 123, 'b': 456, 'c': 789, 'd': 0,   'e': -1},
            {'a': -1,  'b': 0,   'c': 789, 'd': 456, 'e': 123},
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_comments_should_be_ignored(self):
        contents = dedent('''
        #this file is about something
        a\tb\tc\td\te
        int\tint\tint\tstring\tstring
        123\t456\t789\tq\tw
        #2\t5\t8\tq\tw
        3\t6\t7\t#e\t#r
        ''').strip()
        expected = [
            {'a': 123, 'b': 456, 'c': 789, 'd': 'q',   'e': 'w'},
            {'a': 3,  'b': 6,    'c': 7,   'd': '#e',  'e': '#r'},
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_escape_sequences(self):
        backslash = '\\\\'
        tab = '\\t'
        newline = '\\n'
        null = '\\N'
        contents = dedent('''
        a\tb\tc\td\te
        string\tstring\tstring\tstring\tstring
        #a\tb\tc\td\te
        {}\t{}\t{}\t{}\tz
        \#a\tb\tc\td\te
        '''.format(backslash, tab, newline, null)).strip()
        expected = [
            {'a': '\\', 'b': '\t', 'c': '\n', 'd': None, 'e': 'z'},
            {'a': '#a', 'b': 'b',  'c': 'c',  'd': 'd',  'e': 'e'}
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_parse_file(self):
        cities = parse_file('brazilian-cities.row')
        self.assertEqual(len(cities), 5565)

        cities_rio = [city for city in cities if city['state'] == u'RJ']
        self.assertEqual(len(cities_rio), 92)

        types_keys = set([type(key) for city in cities for key in city.keys()])
        self.assertEqual(types_keys, set([unicode]))

        types_state = set([type(city['state']) for city in cities])
        types_name = set([type(city['city']) for city in cities])
        types_inhabitants = set([type(city['inhabitants']) for city in cities])
        types_area = set([type(city['area']) for city in cities])

        self.assertEqual(types_state, set([unicode]))
        self.assertEqual(types_name, set([unicode]))
        self.assertEqual(types_inhabitants, set([int]))
        self.assertEqual(types_area, set([float]))


    def test_type_converters(self):
        contents = dedent(u'''
        b\ti\tf\td\tdt\ts
        bool\tint\tfloat\tdate\tdatetime\tstring

        \\N\t\\N\t\\N\t\\N\t\\N
        true\t42\t6.28\t2014-04-29\t1987-04-29T03:02:00-03:00\tÁlvaro's bday
        false\t42\t6.28\t2014-04-29\t1987-04-29T03:02:00-03:00\tÁlvaro's bday
        ''').strip()
        field_names = ('b', 'i', 'f', 'd', 'dt', 's')

        class UTC_less_3(datetime.tzinfo):
            def utcoffset(self, dt):
                return datetime.timedelta(hours=-3)
            def tzname(self, dt):
                return '-03:00'

        sample_date = datetime.date(2014, 4, 29)
        sample_datetime = datetime.datetime(1987, 4, 29, 3, 2, 0,
                tzinfo=UTC_less_3())

        rows = parse(contents)
        self.assertEqual(len(rows), 3)

        none_row = [None, None, None, None, None]
        self.assertEqual(rows[0], dict(zip(field_names, none_row)))

        expected_row = [True, 42, 6.28, sample_date, sample_datetime,
                u"Álvaro's bday"]
        self.assertEqual(rows[1], dict(zip(field_names, expected_row)))

        expected_row[0] = False
        self.assertEqual(rows[2], dict(zip(field_names, expected_row)))
