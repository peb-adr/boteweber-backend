import mysql.connector
import mysql.connector.cursor
import mysql.connector.errors

import error

conn: mysql.connector.MySQLConnection
curs: mysql.connector.cursor.MySQLCursorDict

CONN_CONFIG = {
    'user': 'boteweber',
    'password': 'boteweber',
    'host': '127.0.0.1'
}
DB_NAME = 'boteweber'
TABLES = dict()
TABLES['news'] = (
    "CREATE TABLE IF NOT EXISTS news ("
    "  id int NOT NULL AUTO_INCREMENT,"
    "  timestamp datetime NOT NULL,"
    "  title text NOT NULL,"
    "  message text NOT NULL,"
    "  PRIMARY KEY (id)"
    ")")
TABLES['info'] = (
    "CREATE TABLE IF NOT EXISTS info ("
    "  id int NOT NULL AUTO_INCREMENT,"
    "  text text NOT NULL,"
    "  greets_he_top text NOT NULL,"
    "  greets_he_bot text NOT NULL,"
    "  greets_moin_top text NOT NULL,"
    "  greets_moin_bot text NOT NULL,"
    "  PRIMARY KEY (id)"
    ")")


def init():
    global conn
    global curs

    try:
        conn = mysql.connector.connect(**CONN_CONFIG)
    except mysql.connector.Error as e:
        print(e)
        exit(1)

    curs = conn.cursor(dictionary=True)
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


def get_news():
    try:
        curs.execute("SELECT * FROM news")
        data = curs.fetchall()
    except mysql.connector.Error:
        raise error.DBError
    return data


def get_news_id(id):
    try:
        curs.execute("SELECT * FROM news WHERE id=%s", (id,))
        data = curs.fetchone()
        if not data:
            raise error.NotFoundError
    except mysql.connector.Error:
        raise error.DBError
    return data


def post_news(data):
    try:
        curs.execute("INSERT INTO news (timestamp, title, message) VALUES (%s, %s, %s)",
                     (data['timestamp'], data['title'], data['message']))
        conn.commit()
        data = get_news_id(curs.lastrowid)
    except mysql.connector.Error:
        raise error.DBError
    return data


def put_news_id(id, data):
    try:
        curs.execute("UPDATE news SET timestamp=%s, title=%s, message=%s WHERE id=%s",
                     (data['timestamp'], data['title'], data['message'], id))
        conn.commit()
        data = get_news_id(id)
    except mysql.connector.Error:
        raise error.DBError
    return data


def delete_news_id(id):
    try:
        data = get_news_id(id)
        curs.execute("DELETE FROM news WHERE id=%s", (id,))
        conn.commit()
    except mysql.connector.Error:
        raise error.DBError
    return data


def get_info_id(id):
    try:
        curs.execute("SELECT * FROM info WHERE id=%s", (id,))
        data = curs.fetchone()
        if not data:
            raise error.NotFoundError
    except mysql.connector.Error:
        raise error.DBError
    return data


def put_info_id(id, data):
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
        data = get_info_id(id)
    except mysql.connector.Error:
        raise error.DBError
    return data
