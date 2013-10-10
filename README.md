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
