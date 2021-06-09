import logging
import os

import psycopg2


logging.basicConfig(
    filename='bot.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_host = 'db'
db_port = '5432'

connection = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port)


def subscribe(values):
    query = """
    SELECT chat_id
    FROM users
    WHERE chat_id='{}';
    """.format(values[0])
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if values[0] in str(rows):
        query = """
        UPDATE users
        SET subscribe=TRUE
        WHERE chat_id='{}';
        """.format(values[0])
    else:
        query = """
        INSERT INTO users
        (chat_id, name, surname, username, status, subscribe, black_list)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')
        """.format(values[0], values[1],
                   values[2], values[3],
                   'user', True, False)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def unsubscribe(value):
    query = """
    UPDATE users
    SET subscribe=FALSE
    WHERE chat_id='{}';
    """.format(value)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def check_url(value):
    query = """
    SELECT COUNT(*)
    FROM urls
    WHERE url='{}';
    """.format(value)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if rows[0][0] == 0:
        reply = 'Администратор рассмотрит вашу заявку'
        result = True
    else:
        reply = 'Такой сайт уже существует в базе данных'
        query = """
        SELECT black_list
        FROM urls
        WHERE url='{}';
        """.format(value)
        cursor.execute(query, connection)
        rows = cursor.fetchall()
        if rows[0][0]:
            reply += '\nНо этот сайт в черном списке'
        result = False
    return (reply, result)


def check_chat(value):
    query = """
    SELECT COUNT(*)
    FROM chats
    WHERE url='{}';
    """.format(value)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if rows[0][0] == 0:
        reply = 'Администратор рассмотрит вашу заявку'
        result = True
    else:
        reply = 'Такой чат уже существует в базе данных'
        query = """
        SELECT black_list
        FROM chats
        WHERE url='{}'
        """.format(value)
        cursor.execute(query, connection)
        rows = cursor.fetchall()
        if rows[0][0]:
            reply += '\nНо этот чат в черном списке'
        result = False
    return (reply, result)


def admin_ids():
    query = """
    SELECT chat_id
    FROM users
    WHERE status='admin';
    """
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    return result
