import logging
import os

import psycopg2


logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
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
