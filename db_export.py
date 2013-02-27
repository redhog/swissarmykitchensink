#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

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

args = dict([arg.split('=', 1) for arg in sys.argv[1:]])

expr = args['expr']
del args['expr']

connector = "postgres"
if "conn" in args:
    connector = args['conn']
    del args['conn']

connectors = {
    'mysql': 'MySQLdb',
    'postgres': 'pyPgSQL.PgSQL'}

connector = connectors.get(connector, connector)
module = __import__(connector)
for name in connector.split('.')[1:]:
    module = getattr(module, name)

conn = module.connect(**args)

cur = conn.cursor()

writer = csv.writer(sys.stdout)

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
        writer.writerow(row)
        row = cur.fetchone()

if "%" in expr:
    reader = csv.reader(sys.stdin)
    columns = reader.next()
    for row in reader:
        row = dict(zip(columns, row))
        execute(row)
else:
    execute()

conn.commit()