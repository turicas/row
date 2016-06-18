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
