# coding: utf-8

import datetime

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
        'string': lambda value: value if value is not None else None,}


def _filter_escape_sequences(value):
    if value == '\\N':
        return None
    else:
        return value.replace('\\t', '\t').replace('\\n', '\n')\
                    .replace('\\#', '#').replace('\\\\', '\\')

def _validate_types(field_types):
    return all([field_type in TYPE_CONVERTERS for field_type in field_types])


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
