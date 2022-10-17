
import sqlite3



import click
import sys
import traceback
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'sqlite.db'
            # detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

        try:
            with current_app.open_resource('schema.sql') as f:
                g.db.executescript(f.read().decode('utf8'))
            print("Finished writing schemas")
        except:
            print("Schemas already present")


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


# ### INSERTERS

def new_owner(name, email):
    print('adding new user')
    try:
        with sqlite3.connect('dbase.db') as dbs:
            dbs.cursor().execute(f"insert into user values('{name}','{email}');")
            dbs.commit()
        print(0)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def new_list(title, color, owner):
    print('adding new list')
    try:
        with sqlite3.connect('dbase.db') as dbs:
            dbs.cursor().execute(f"insert into list(title, color,owner) values('{title}','{color}','{owner}');")
            dbs.commit()
        print(0)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def new_card(title, content, status, deadline, parent_list):
    print('adding new card')
    try:
        with sqlite3.connect('dbase.db') as dbs:
            dbs.cursor().execute(
                f"insert into card(title, content,status,deadline,parent_list) values('{title}', '{content}', '{status}', '{deadline}', '{parent_list}');")
            dbs.commit()
        print(0)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


# ### GETTERS

def this_card(mid):
    try:
        output = []
        with sqlite3.connect('dbase.db') as dbs:
            lists = dbs.cursor().execute(
                f"select title,content, status,deadline,parent_list from card where id='{mid}'")
        for r in lists:
            output.append(r)
        print(0)
        return output
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def get_card(mlist):  # get all cards of a list
    output = []
    with sqlite3.connect('dbase.db') as dbs:
        lists = dbs.cursor().execute(f"select title, status from card where parent_list='{mlist}'")
    for r in lists:
        output.append(r)
    return output


def dashboard(owner):
    try:
        output = []
        with sqlite3.connect('dbase.db') as dbs:
            lists = dbs.cursor().execute(f"select title,id from list where owner='{owner}'")
        for r in lists:
            output.append({'title': r[0], 'child': get_card(r[1]), 'id': r[1]})
            dbs.commit()
        print(0)
        return output
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


# ### DELETERS

def delete_card(mid):
    print('deleting a card')
    try:
        with sqlite3.connect('dbase.db') as dbs:
            dbs.cursor().execute(f"delete from card where id='{mid}';")
            dbs.commit()
        print(0)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def delete_list(mid):
    print('deleting a list')
    try:
        with sqlite3.connect('dbase.db') as dbs:
            dbs.cursor().execute(f"delete from list where id='{mid}';")
            dbs.commit()
        print(0)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

# new_owner('Shamlee','shamlee@cute.com')
# new_list('Garden', "green",'shamlee@cute.com')
# new_card('remove weeds',"care the plants",2,4354,1)

# print(dashboard('shamlee@cute.com'))
# delete_card(5)

# init_db()