# coding: utf-8

import datetime
import gzip

from base64 import b64decode, b64encode
from collections import OrderedDict

import iso8601


def _convert_date(date_str):
    if date_str is None:
        return None
    return datetime.date(*[int(x) for x in date_str.split('-')])


def _convert_bool(bool_str):
    if bool_str is None:
        return None
    return bool_str.lower() == 'true'


def _convert_datetime(datetime_str):
    if datetime_str is None:
        return None
    return iso8601.parse_date(datetime_str)


TYPE_CONVERTERS = {
        'bool': _convert_bool,
        'int': lambda value: int(value) if value is not None else None,
        'float': lambda value: float(value) if value is not None else None,
        'date': _convert_date,
        'datetime': _convert_datetime,
        'text': lambda value: value if value is not None else None,
        'binary': lambda value: b64decode(value) if value is not None else None, }

def _bool_serializer(value):
    if value is True:
        return 'true'
    elif value is False:
        return 'false'
    else:
        return None

def _number_serializer(value):
    if value is not None:
        return str(value)
    else:
        return None

def _time_serializer(value):
    if value is not None:
        return value.isoformat()
    else:
        return None

def _text_serializer(value):
    return value

def _binary_serializer(value):
    if value is not None:
        return b64encode(value)
    else:
        return None

TYPE_SERIALIZER = {
        'bool': _bool_serializer,
        'int': _number_serializer,
        'float': _number_serializer,
        'date': _time_serializer,
        'datetime': _time_serializer,
        'text': _text_serializer,
        'binary': _binary_serializer, }


def _filter_escape_sequences(value):
    if value == '\\N':
        return None
    else:
        return value.replace('\\t', '\t').replace('\\n', '\n')\
                    .replace('\\#', '#').replace('\\\\', '\\')

def _validate_types(field_types):
    return all([field_type in TYPE_CONVERTERS for field_type in field_types])


def _fix_value(value):
    if value is None:
        return '\\N'
    else:
        return value.replace('\t', '\\t').replace('\n', '\\n')\
                    .replace('#', '\\#').replace('\\', '\\\\')

def _create_line(values):
    return '\t'.join(_fix_value(value) for value in values) + '\n'


def _create_row(values, fieldtypes):
    return _create_line(TYPE_SERIALIZER[fieldtype](value)
                        for fieldtype, value in zip(fieldtypes, values))


def _convert_types(values, types):
    return [TYPE_CONVERTERS[type_](value)
            for type_, value in zip(types, values)]


def parse(text):
    rows = [map(_filter_escape_sequences, line.split('\t'))
            for line in text.split('\n')
            if not line.startswith('#') and line.strip()]
    field_names, field_types = rows[0:2]

    if len(rows) < 2 or not _validate_types(field_types):
        raise ValueError('Incorrect format')

    return [dict(zip(field_names, _convert_types(row, field_types)))
            for row in rows[2:]]


def parse_file(filename):
    with open(filename) as fobj:
        return parse(fobj.read().decode('utf-8'))


class Reader(object):

    def __init__(self, fobj):
        self._gzip = False
        self._fobj = fobj
        data = self._fobj.read(2)
        self._fobj.seek(self._fobj.tell() - 2)
        if data == b'\x1f\x8b':  # gzip
            self._fobj = gzip.open(fobj)
            self._gzip = True

        self._fieldnames = self._take_next()
        self._fieldtypes = self._take_next()
        self._fields = OrderedDict([name_type
            for name_type in zip(self._fieldnames, self._fieldtypes)])

    @property
    def fieldnames(self):
        return self._fieldnames

    @property
    def fieldtypes(self):
        return self._fieldtypes

    @property
    def fields(self):
        return self._fields

    def _take_next(self):
        data = None
        for line in self._fobj:
            if self._gzip:
                line = line.decode('utf-8')
            lstrip = line.strip()
            if lstrip and not lstrip.startswith('#'):
                return [_filter_escape_sequences(value)
                        for value in line[:-1].split('\t')]
        raise StopIteration()

    def __iter__(self):
        return self

    def __next__(self):
        return _convert_types(self._take_next(), self._fieldtypes)

    next = __next__


class DictReader(Reader):

    def __next__(self):
        return dict(zip(self._fieldnames,
                        _convert_types(self._take_next(), self._fieldtypes)))


class Writer(object):

    def __init__(self, fobj, fieldnames, fieldtypes):
        self._fobj = fobj
        self._fieldnames = fieldnames
        self._fieldtypes = fieldtypes
        self._fields = OrderedDict([name_type
            for name_type in zip(fieldnames, fieldtypes)])
        self._fieldcount = len(fieldnames)
        if self._fieldcount != len(fieldtypes):
            raise ValueError('Field names and types should have same length')

        fobj.write(_create_line(fieldnames))
        fobj.write(_create_line(fieldtypes))

    @property
    def fieldnames(self):
        return self._fieldnames

    @property
    def fieldtypes(self):
        return self._fieldtypes

    @property
    def fields(self):
        return self._fields

    def writerow(self, data):
        if len(data) != self._fieldcount:
            raise ValueError('Wrong number of field values')

        self._fobj.write(_create_row(data, self._fieldtypes))

    def close(self):
        self._fobj.close()


class DictWriter(Writer):

    def writerow(self, data):
        if len(data) != self._fieldcount:
            raise ValueError('Wrong number of field values')

        data_values = [data[fieldname] for fieldname in self._fieldnames]
        self._fobj.write(_create_row(data_values, self._fieldtypes))
