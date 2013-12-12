row
===

It's a reference implementation of the new tabular file standard [discussed at
dataprotocols
repository](https://github.com/dataprotocols/dataprotocols/issues/76).

It looks like a [CSV](http://en.wikipedia.org/wiki/Comma-separated_values) but
have stronger rules, lowering ambiguation and complexity of processing (see
"Specification" below).


Specification
-------------

- The first line must be the header;
- Rows must be separated by character `0x0A` (new line, often represented as
  `\n`). **Any** `0x0A` in the file **are row separators** (no exceptions);
- Fields must be separated by `0x09` (tabular space, often represented as
  `0x09`). **Any** `0x09` in the file **are field separators** (no exceptions);
- Field values must be encoded in UTF-8 without BOM (byte-order-marker).
  Binary data should be encoded as base64 or any other format that uses UTF-8
  (or a subset of it, like ASCII) as output;
- A line starting with `#` is considered a comment and must be completely
  ignored by the parser (in any other position `#` is considered data);
- Escape sequences for use inside field data:
  - `\n` for new line (`0x0A`),
  - `\t` for tabular space (`0x09`),
  - `\N` for null (absence of data),
  - `\#` to start a new row with `#` as the first character of the first field,
  - `\\` for back slash (`0x5C`).


Example of Usage
----------------

Giving the file `brazilian-cities.row`, we can read it like this:

    # coding: utf-8

    import row


    cities = row.parse_file('brazilian-cities.row')
    cities_rio = [city for city in cities if city['state'] == u'RJ']
    for city_data in cities_rio:
        area = float(city_data['area'])
        inhabitants = int(city_data['inhabitants'])
        density = inhabitants / area
        print(u'{}:'.format(city_data['city']))
        print(u'  area        = {:8.2f} km²'.format(area))
        print(u'  inhabitants = {:8d} citizens'.format(inhabitants))
        print(u'  density     = {:8.2f} citizens/km²'.format(density))



Tests
-----

First be sure you installed all dependencies:

    pip install -r requirements-development.txt

Then, to run the tests, just execute:

    make test
