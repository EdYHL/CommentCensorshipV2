import pymysql


def load_from_db(table_name: str, database: str) -> set:
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='&amp;f|[c,j/tH#]BK9', db=database)
    cursor = connection.cursor()
    cursor.execute('SELECT word FROM ' + table_name)
    word_list_db = list(cursor.fetchall())
    word_list = set()
    for pair in word_list_db:
        word_list.add(pair[0])
    cursor.close()
    connection.close()
    return word_list
