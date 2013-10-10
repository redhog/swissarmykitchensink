#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# SETUPTOOLS_DO_NOT_WRAP

# db_export database .csv-export/import script
#
#  - Copyright (C) 2007 FreeCode AS, Egil Moeller <egil.moller@freecode.no>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys, csv

if len(sys.argv) == 1:
    print """
Usage:

db_export.py expr="select * from foo" > file.csv
db_export.py expr="insert into foo (bar, fie) values(%(bar)s, %(fie)s)" < file.csv

Other parameters:
conn=psycopg2
conn=pyPgSQL.PgSQL
conn=MySQLdb

Connection parameters (same name as to the connect() function of the
respective driver:
host=localhost
user=username
passwd=password
db=dbname

"""
    sys.exit(0)

args = dict([arg.split('=', 1) for arg in sys.argv[1:]])

expr = args['expr']
del args['expr']

connector = "psycopg2"
if "conn" in args:
    connector = args['conn']
    del args['conn']

module = __import__(connector)
for name in connector.split('.')[1:]:
    module = getattr(module, name)

conn = module.connect(**args)

cur = conn.cursor()

writer = csv.writer(sys.stdout)

def transform_to_csv(item):
    if item is None:
        return '__None__'
    elif item is True:
        return '__True__'
    elif item is False:
        return '__False__'
    return item

def transform_from_csv(item):
    if item == '__None__':
        return None
    elif item == '__True__':
        return True
    elif item == '__False__':
        return False
    return item

def execute(params = {}):
    cur.execute(expr, params)
    row = None
    try:
        row = cur.fetchone()
    except:
        pass
    if row:
        cols = [dsc[0] for dsc in cur.description]
        writer.writerow(cols)
    while row:
        writer.writerow([transform_to_csv(item) for item in row])
        row = cur.fetchone()

if "%" in expr:
    reader = csv.reader(sys.stdin)
    columns = reader.next()
    for row in reader:
        row = dict(zip(columns, [transform_from_csv(item) for item in row]))
        execute(row)
else:
    execute()

conn.commit()
