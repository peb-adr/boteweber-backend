import rest
import sql

if __name__ == '__main__':
    sql.init()

    # sql.delete_news_id(6)

    rest.serve()

    # xd = sql.post_news({'timestamp': datetime(1997, 11, 19), 'title': 'Hello there', 'message': 'IM ALIVE!'})
    # xd = sql.post_news({'timestamp': datetime(1997, 11, 20), 'title': 'Hello there1', 'message': 'IM ALIVE!'})
    # xd = sql.post_news({'timestamp': datetime.now(), 'title': 'Hello there2', 'message': 'IM ALIVE!'})
    # xd = sql.get_news_id(1)
    # print(xd)
