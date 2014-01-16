# db_export
A simple utility to export and import CSV data to/from any sql database supported by a DB API 2.0 compatible python library.

Usage:

    db_export.py expr="select * from foo" > file.csv
    db_export.py expr="insert into foo (bar, fie) values(%(bar)s, %(fie)s)" < file.csv

Other parameters:

    conn=psycopg2
    conn=pyPgSQL.PgSQL
    conn=MySQLdb
    format=kml

Connection parameters (same name as to the connect() function of the respective driver:

    host=localhost
    user=username
    passwd=password
    db=dbname

# skyconvert
Converts between various data list containers. Supported formats:

    json (list containing objects)
    geojson (features with properties)
    csv (optionally containing json in some columns)

Can for example be used to convert between Pybossa tasks.json format and a geojson
container format allowing you to sort through and filter the tasks visually in
e.g. QGis, and then convert them back for import into Pybossa.

Usages:

    convert.py INFILE OUTFILE

Examples:

    convert.py tasks.json tasks.geojson
    convert.py tasks.geojson tasks.json
    convert.py tasks.geojson tasks.csv
    convert.py tasks.csv tasks.json

# jsonedit
Edits json files using jsonpaths

For more information on jsonpaths see http://goessner.net/articles/JsonPath/

There are three possible usages:

    jsonedit.py infile.json outfile.json '$..bbox'

This will compile a list of all bbox attribute values

    jsonedit.py infile.json outfile.json '$..options' '{"layer": "47-11"}'

This will replace all options attribute values with the json object {"layer": "47-11"}

    jsonedit.py infile.json outfile.json '$..bbox' delete

This will delete all bbox attributes
