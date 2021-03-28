"""
db utilities
This links dbs with the g object, making it convenient to work with the db from
our views.
The code is taken from examples in the flask documentation
"""

import sqlite3
from flask import g, current_app

def make_dicts(cursor, row):
    """convert rows to dictionary"""
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        #g.db.row_factory = sqlite3.Row #alternative to dicts will make namedtuples
        g.db.row_factory = make_dicts

    return g.db

def query_db(query, args=(), one=False):
    """
    convenience function to run a query and get results in one go
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

#def init_db():
#    """Clear existing data and create new tables."""
#    db = get_db()
#
#    with current_app.open_resource("schema.sql") as f:
#        db.executescript(f.read().decode("utf8"))

def init_app(app):
    app.teardown_appcontext(close_db)
    #app.cli.add_command(init_db_command)

#@click.command("init-db")
#@with_appcontext
#def init_db_command():
#    """Clear existing data and create new tables."""
#    init_db()
#    click.echo("Initialized the database.")
