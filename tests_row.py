# coding: utf-8

import os
import tempfile
import unittest

from textwrap import dedent

from row import parse, parse_file


class TestTab(unittest.TestCase):
    def test_no_records(self):
        contents = dedent('''
        a\tb\tc\td\te
        ''').strip()
        expected = []
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_normal_records(self):
        contents = dedent('''
        a\tb\tc\td\te
        123\t456\t789\t0\t-1
        -1\t0\t789\t456\t123
        ''').strip()
        expected = [
            {'a': '123', 'b': '456', 'c': '789', 'd': '0',   'e': '-1'},
            {'a': '-1',  'b': '0',   'c': '789', 'd': '456', 'e': '123'},
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_empty_lines(self):
        contents = dedent('''
        a\tb\tc\td\te
        123\t456\t789\t0\t-1


        -1\t0\t789\t456\t123
        ''').strip() + '\n'
        expected = [
            {'a': '123', 'b': '456', 'c': '789', 'd': '0',   'e': '-1'},
            {'a': '-1',  'b': '0',   'c': '789', 'd': '456', 'e': '123'},
        ]
        result = parse(contents)
        self.assertEqual(result, expected)

    def test_comments(self):
        contents = dedent('''
        a\tb\tc\td\te
        123\t456\t789\tq\tw
        #2\t5\t8\tq\tw
        3\t6\t#7\te\tr
        ''').strip()
        expected = [
            {'a': '123', 'b': '456', 'c': '789', 'd': 'q', 'e': 'w'},
            {'a': '3',   'b': '6',   'c': '#7',  'd': 'e', 'e': 'r'}
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
        temporary = tempfile.NamedTemporaryFile(delete=False)
        contents = dedent('''
        a\tb\tc\td\te
        123\t456\t789\t0\t-1
        -1\t0\t789\t456\t123
        ''').strip() + '\n'
        temporary.write(contents)
        temporary.close()
        expected = [
            {'a': '123', 'b': '456', 'c': '789', 'd': '0',   'e': '-1'},
            {'a': '-1',  'b': '0',   'c': '789', 'd': '456', 'e': '123'},
        ]
        result = parse_file(temporary.name)
        os.unlink(temporary.name)
        self.assertEqual(result, expected)
