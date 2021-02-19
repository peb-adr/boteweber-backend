from threading import Lock

import mysql.connector
import mysql.connector.cursor
import mysql.connector.errors

from src import error
from src import schema
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


def select(schema_name, orderby=None, page=None):
    d = schema.get(schema_name)

    lock.acquire()
    try:
        # non relational
        query_orderby = " ORDER BY " + ", ".join(orderby) if orderby else ""
        query_limit = " LIMIT " + str((page[0] - 1) * page[1]) + "," + str(page[1]) if page else ""
        curs.execute("SELECT * FROM " + d['title'] + query_orderby + query_limit)
        data = curs.fetchall()
        # relational
        for d in data:
            d.update(select_relational_by_id(schema_name, d['id']))
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()

    return data


def select_ids(schema_name):
    d = schema.get(schema_name)

    lock.acquire()
    try:
        curs.execute("SELECT id FROM " + d['title'])
        data = curs.fetchall()
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()

    # extract ids from dicts into a list
    return [d['id'] for d in data]


def select_by_id(schema_name, id):
    d = schema.get(schema_name)

    lock.acquire()
    try:
        # non relational
        curs.execute("SELECT * FROM " + d['title'] + " WHERE id=%s", (id,))
        data = curs.fetchone()
        if not data:
            raise error.NotFoundError("Item with id=" + str(id) + " not found in " + d['title'])
        # relational
        data.update(select_relational_by_id(schema_name, id))
    except mysql.connector.Error as e:
        raise error.DBError(e.msg)
    finally:
        lock.release()

    return data


def insert(schema_name, data):
    d = schema.get(schema_name)
    nonrel_data = schema.get_instance_non_relational_data(schema_name, data)

    lock.acquire()
    try:
        # ensure a new entry gets assigned a new id by the DB
        if 'id' in nonrel_data:
            del nonrel_data['id']
        # non relational
        cols = util.commasep_formatted_list(nonrel_data, "{0}")
        vals = util.commasep_formatted_list(nonrel_data, "%({0})s")
        curs.execute("INSERT INTO " + d['title'] + " (" + cols + ") VALUES (" + vals + ")", nonrel_data)
        lastrowid = curs.lastrowid
        # relational
        insert_relational(schema_name, data)
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise error.DBError(e.errno)
    except error.NotFoundError as e:
        conn.rollback()
        raise e
    finally:
        lock.release()

    data = select_by_id(schema_name, lastrowid)
    return data


def update_by_id(schema_name, id, data):
    d = schema.get(schema_name)
    nonrel_data = schema.get_instance_non_relational_data(schema_name, data)

    # check if exists
    select_by_id(schema_name, id)
    lock.acquire()
    try:
        # ensure id can not be changed
        nonrel_data['id'] = id
        # non relational
        assigns = util.commasep_formatted_list(nonrel_data, "{0}=%({0})s")
        curs.execute("UPDATE " + d['title'] + " SET " + assigns + " WHERE id=%(id)s", nonrel_data)
        # relational
        delete_relational_by_id(schema_name, id)
        insert_relational(schema_name, data, id)
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise error.DBError(e.msg)
    except error.NotFoundError as e:
        conn.rollback()
        raise e
    finally:
        lock.release()

    data = select_by_id(schema_name, id)
    return data


def delete_by_id(schema_name, id):
    d = schema.get(schema_name)

    data = select_by_id(schema_name, id)
    lock.acquire()
    try:
        # non relational
        curs.execute("DELETE FROM " + d['title'] + " WHERE id=%s", (id,))
        # relational
        delete_relational_by_id(schema_name, id)
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise error.DBError(e.msg)
    except error.NotFoundError as e:
        conn.rollback()
        raise e
    finally:
        lock.release()

    return data


def select_relational_by_id(schema_name, id):
    d = schema.get(schema_name)
    rel_props = schema.get_relational_properties(schema_name)
    rel_data = dict()

    for p in rel_props:
        curs.execute("SELECT " + p + "_id" +
                     " FROM " + d['title'] + "_" + p +
                     " WHERE " + d['title'] + "_id" + "=%s", (id,))
        data = curs.fetchall()
        # unpack list of dict
        rel_data[p] = list()
        for sel in data:
            rel_data[p].append(sel[p + "_id"])

    return rel_data


def insert_relational(schema_name, data, id=None):
    d = schema.get(schema_name)
    rel_data = schema.get_instance_relational_data(schema_name, data)

    my_id = id if id is not None else curs.lastrowid
    for p in rel_data:
        for rel_id in rel_data[p]:
            cols = d['title'] + "_id, " + p + "_id"
            vals = "%s, %s"
            try:
                # forward relation
                curs.execute("INSERT INTO " + d['title'] + "_" + p + " (" + cols + ") " +
                             "VALUES (" + vals + ")", (my_id, rel_id))
                # backward relation
                curs.execute("INSERT INTO " + p + "_" + d['title'] + " (" + cols + ") " +
                             "VALUES (" + vals + ")", (my_id, rel_id))
            except mysql.connector.Error as e:
                if e.errno == 1452:
                    raise error.NotFoundError("Item with id=" + str(rel_id) + " not found in " + p)
                else:
                    raise e


def delete_relational_by_id(schema_name, id):
    d = schema.get(schema_name)
    rel_props = schema.get_relational_properties(schema_name)

    for p in rel_props:
        try:
            # forward relation
            curs.execute("DELETE FROM " + d['title'] + "_" + p +
                         " WHERE " + d['title'] + "_id" + "=%s", (id,))
            # backward relation
            curs.execute("DELETE FROM " + p + "_" + d['title'] +
                         " WHERE " + d['title'] + "_id" + "=%s", (id,))
        except mysql.connector.Error as e:
            if e.errno == 1452:
                raise error.NotFoundError("Item with id=" + str(id) + " not found in " + p)
            else:
                raise e
