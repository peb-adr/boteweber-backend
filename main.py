import sql
from datetime import date

if __name__ == '__main__':
    sql.init()

    xd = sql.post_news({'timestamp': date(1997, 11, 19), 'title': 'Hello there', 'message': 'IM ALIVE!'})
    xd = sql.post_news({'timestamp': date(1997, 11, 20), 'title': 'Hello there1', 'message': 'IM ALIVE!'})
    xd = sql.post_news({'timestamp': date(1997, 11, 21), 'title': 'Hello there2', 'message': 'IM ALIVE!'})
    xd = sql.get_news_id(1)
    print(xd)
