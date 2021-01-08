import mysql.connector
import mysql.connector.cursor
import mysql.connector.errors
from threading import Lock

from src import error
from src import util

conn: mysql.connector.MySQLConnection
curs: mysql.connector.cursor.MySQLCursorDict

lock: Lock

DB_NAME = 'boteweber'
TABLES = {
    'news': (
        "CREATE TABLE IF NOT EXISTS news ("
        "  id int NOT NULL AUTO_INCREMENT,"
        "  timestamp datetime NOT NULL,"
        "  title text NOT NULL,"
        "  message text NOT NULL,"
        "  PRIMARY KEY (id)"
        ")"
    ),
    'info': (
        "CREATE TABLE IF NOT EXISTS info ("
        "  id int NOT NULL AUTO_INCREMENT,"
        "  text text NOT NULL,"
        "  greets_he_top text NOT NULL,"
        "  greets_he_bot text NOT NULL,"
        "  greets_moin_top text NOT NULL,"
        "  greets_moin_bot text NOT NULL,"
        "  PRIMARY KEY (id)"
        ")"
    )
}


def init(conn_config):
    global conn
    global curs
    global lock

    try:
        conn = mysql.connector.connect(**conn_config)
    except mysql.connector.Error as e:
        print(e)
        exit(1)

    curs = conn.cursor(dictionary=True, buffered=True)
    try:
        curs.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as e:
        print(e)
        exit(1)

    for t in TABLES.values():
        try:
            curs.execute(t)
            conn.commit()
        except mysql.connector.Error as e:
            print(e)
            exit(1)

    lock = Lock()


def select(table):
    lock.acquire()
    try:
        curs.execute("SELECT * FROM " + table)
        data = curs.fetchall()
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()
    return data


def select_by_id(table, id):
    lock.acquire()
    try:
        curs.execute("SELECT * FROM " + table + " WHERE id=%s", (id,))
        data = curs.fetchone()
        if not data:
            raise error.NotFoundError("Item with id=" + str(id) + " not found in " + table)
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()
    return data


def insert(table, data):
    lock.acquire()
    try:
        # ensure a new entry gets assigned a new id by the DB
        if 'id' in data:
            del data['id']
        cols = util.commasep_formatted_list(data, "{0}")
        vals = util.commasep_formatted_list(data, "%({0})s")
        curs.execute("INSERT INTO " + table + " (" + cols + ") VALUES (" + vals + ")", data)
        conn.commit()
    except mysql.connector.Error as e:
        raise error.DBError(e.errno)
    finally:
        lock.release()
    data = select_by_id(table, curs.lastrowid)
    return data


def update_by_id(table, id, data):
    # check if exists
    select_by_id(table, id)
    lock.acquire()
    try:
        # ensure id can not be changed
        data['id'] = id
        assigns = util.commasep_formatted_list(data, "{0}=%({0})s")
        curs.execute("UPDATE " + table + " SET " + assigns + " WHERE id=%(id)s", data)
        conn.commit()
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()
    data = select_by_id(table, id)
    return data


def delete_by_id(table, id):
    data = select_by_id(table, id)
    lock.acquire()
    try:
        curs.execute("DELETE FROM " + table + " WHERE id=%s", (id,))
        conn.commit()
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()
    return data
