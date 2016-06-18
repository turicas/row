# coding: utf-8

# Copyright 2016 Álvaro Justen <https://github.com/turicas/rows/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup


LONG_DESCRIPTION = '''
No matter in which format your tabular data is: rows will import it,
automatically detect types and give you high-level Python objects so you can
start working with the data instead of trying to parse it. It is also
locale-and-unicode aware. :)

See a quick start tutorial at:
    https://github.com/turicas/rows/blob/develop/README.md
'''.strip()


setup(name='row',
      description='A brand-new tabular format',
      long_description=LONG_DESCRIPTION,
      version='0.1.0dev',
      author=u'Álvaro Justen',
      author_email='alvarojusten@gmail.com',
      url='https://github.com/turicas/row/',
      py_modules=['row'],
      install_requires=['iso8601'],
      keywords=['tabular', 'table', 'row', 'xls', 'xlsx', 'csv', 'rows',],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Database',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ]
)
