import mysql.connector
import mysql.connector.cursor
import mysql.connector.errors

from src import error

conn: mysql.connector.MySQLConnection
curs: mysql.connector.cursor.MySQLCursorDict

locked: bool

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
    global locked

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

    locked = False


def lock():
    global locked

    while locked:
        pass
    locked = True


def unlock():
    global locked

    locked = False


def get_news():
    lock()
    try:
        curs.execute("SELECT * FROM news")
        data = curs.fetchall()
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    return data


def get_news_id(id):
    lock()
    try:
        curs.execute("SELECT * FROM news WHERE id=%s", (id,))
        data = curs.fetchone()
        if not data:
            raise error.NotFoundError
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    return data


def post_news(data):
    lock()
    try:
        curs.execute("INSERT INTO news (timestamp, title, message) VALUES (%s, %s, %s)",
                     (data['timestamp'], data['title'], data['message']))
        conn.commit()
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    data = get_news_id(curs.lastrowid)
    return data


def put_news_id(id, data):
    lock()
    try:
        curs.execute("UPDATE news SET timestamp=%s, title=%s, message=%s WHERE id=%s",
                     (data['timestamp'], data['title'], data['message'], id))
        conn.commit()
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    data = get_news_id(id)
    return data


def delete_news_id(id):
    data = get_news_id(id)
    lock()
    try:
        curs.execute("DELETE FROM news WHERE id=%s", (id,))
        conn.commit()
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    return data


def get_info_id(id):
    lock()
    try:
        curs.execute("SELECT * FROM info WHERE id=%s", (id,))
        data = curs.fetchone()
        if not data:
            raise error.NotFoundError
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    return data


def put_info_id(id, data):
    lock()
    try:
        curs.execute("UPDATE info SET "
                     "text=%s, "
                     "greets_he_top=%s, "
                     "greets_he_bot=%s, "
                     "greets_moin_top=%s, "
                     "greets_moin_bot=%s WHERE id=%s",
                     (data['text'],
                      data['greets_he_top'],
                      data['greets_he_bot'],
                      data['greets_moin_top'],
                      data['greets_moin_bot'],
                      id))
        conn.commit()
    except mysql.connector.Error:
        raise error.DBError
    unlock()
    data = get_info_id(id)
    return data
