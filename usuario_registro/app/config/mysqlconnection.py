import os

import pymysql.cursors

class MySQLConnection:
    def __init__(self):

        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'Santiago2023', 
                                    db = "usuarios_registro",
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)

        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:

                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:

                    result = cursor.fetchall()
                    return result
                else:

                    self.connection.commit()
            except Exception as e:

                print("Something went wrong", e)
                return False
            finally:

                self.connection.close() 

def connectToMySQL():
    return MySQLConnection()