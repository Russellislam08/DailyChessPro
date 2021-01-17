''' database abstraction layer '''

import os
from pprint import pprint

import pymysql

import mysql.connector
from mysql.connector.constants import ClientFlag

DB_USER = os.environ.get('CLOUD_SQL_USERNAME')
DB_PASSWORD = os.environ.get('CLOUD_SQL_PASSWORD')
DB_NAME = os.environ.get('CLOUD_SQL_DATABASE_NAME')
DB_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
DB_HOST = os.environ.get('CLOUD_SQL_CONNECTION_HOST')
TABLE_NAME = os.environ.get('DB_TABLE_NAME', None)


# Queries
SELECT_QUERY = ''' SELECT user_id FROM test; '''
SELECT_SPECIFIC_USER_QUERY = ''' SELECT user_id FROM test WHERE user_id = %s; '''
INSERT_QUERY = 'INSERT INTO test (user_id) VALUES (%s);'
DELETE_QUERY = 'DELETE FROM test WHERE user_id = %s;'


def create_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)


def get_cursor(conn):
    return conn.cursor(pymysql.cursors.DictCursor)

def get_all_users():
    conn = None
    response = None
    try:
        conn = create_connection()
        c = get_cursor(conn)

        c.execute(SELECT_QUERY);
        response = c.fetchall()

        pprint(response)
    except Exception as e:
        print(e)
        return []
    else:
        return response
    finally:
        if conn:
            conn.close()


def get_user(user_id):
    conn = None
    response = None
    try:
        conn = create_connection()
        c = get_cursor(conn)

        c.execute(SELECT_SPECIFIC_USER_QUERY, (user_id,));
        response = c.fetchall()
        pprint(response)
    except Exception as e:
        print(e)
        return []
    else:
        return response
    finally:
        if conn:
            conn.close()

def add_user(user_id):
    conn = None
    try:
        conn = create_connection()
        c = get_cursor(conn)

        c.execute(INSERT_QUERY, (user_id,));
        conn.commit()


    except Exception as e:
        print(e)
        return []

    finally:
        if conn:
            conn.close()

def delete_user(user_id):
    conn = None
    try:
        conn = create_connection()
        c = get_cursor(conn)

        c.execute(DELETE_QUERY, (user_id,));
        conn.commit()

    except Exception as e:
        print(e)
        return []

    finally:
        if conn:
            conn.close()





# if __name__ == '__main__':
#     print("I AM DOING THIS")

#     print("This happens before")
#     # get_all_users()
#     # add_user('iamtestingthisid')
#     get_all_users()
#     print("This happens after")

#     print("I am happening before AGAIN")
#     delete_user('iamtestingthisid')
#     get_all_users()
#     print("I am happening after AGAIN")


