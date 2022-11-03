import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'sqlite.db'
            # detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = row_to_dict
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    try:
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        print("Finished writing schemas")
    except:
        print("Schemas already present")


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
