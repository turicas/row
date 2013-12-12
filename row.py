# coding: utf-8


def _filter_escape_sequences(value):
    if value == '\\N':
        return None
    else:
        return value.replace('\\t', '\t').replace('\\n', '\n')\
                    .replace('\\#', '#').replace('\\\\', '\\')


def parse(text):
    rows = [map(_filter_escape_sequences, line.split('\t'))
            for line in text.split('\n')
            if not line.startswith('#') and line.strip()]
    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:]]


def parse_file(filename):
    with open(filename) as fobj:
        return parse(fobj.read().decode('utf-8'))
