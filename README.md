# row

It's a reference implementation of the new tabular file standard [discussed at
dataprotocols
repository](https://github.com/dataprotocols/dataprotocols/issues/76).

It looks like a [CSV](http://en.wikipedia.org/wiki/Comma-separated_values) but
have stronger rules, lowering ambiguation and complexity of processing (see
"Specification" below).


## Specification

- Blank lines or lines starting with `#` are discarded by the parser;
- The first valid line must be the header;
- The second valid line must be the field types;
- Rows must be separated by character `0x0A` (new line, often represented as
  `\n`). **Any** `0x0A` in the file **are row separators** (no exceptions);
- Fields must be separated by `0x09` (tabular space, often represented as
  `0x09`). **Any** `0x09` in the file **are field separators** (no exceptions);
- Field values must be encoded in UTF-8 without BOM (byte-order-marker).
  Binary data should be encoded as base64 or any other format that uses UTF-8
  (or a subset of it, like ASCII) as output;
- Escape sequences for use inside field data:
  - `\n` for new line (`0x0A`),
  - `\t` for tabular space (`0x09`),
  - `\N` for null (absence of data),
  - `\#` to start a new row with `#` as the first character of the first field,
  - `\\` for back slash (`0x5C`).
- The file could be or could not be gzip-compressed (the parser should detect
  automatically)


### Field Types

- `bool`
- `int`
- `float`
- `date`
- `datetime`
- `text`
- `binary`


## Example of Usage

The interface looks like Python's `csv` module: has `DictReader` and
`DictWriter` classes.

Giving the file `brazilian-cities.row`, we can read it like this:

```python
# coding: utf-8

import row

cities = row.DictReader(open('brazilian-cities.row', 'rb'))
for city in cities:
    if city['state'] != 'RJ':
        continue
    area = city['area']
    inhabitants = city['inhabitants']
    density = inhabitants / area
    print('{}:'.format(city['city']))
    print('  area        = {:8.2f} km²'.format(area))
    print('  inhabitants = {:8d} citizens'.format(inhabitants))
    print('  density     = {:8.2f} citizens/km²'.format(density))
```



## TODO

### Specification

- Support for variable (unknown) metadata
- Support for format versioning metadata
- May add optional RDF metadata
- Add 'binary' type (base64-encoded)


### Python Library

- Python3 support


## Tests

First be sure you installed all dependencies:

    pip install -r requirements-development.txt

Then, to run the tests, just execute:

    make test
