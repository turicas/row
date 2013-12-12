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
