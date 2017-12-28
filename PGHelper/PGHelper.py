class PGHelper():
    import time
    import psycopg2
    import os

    def __init__(self, host=False, dbname=False, user=False, password=False, port=False):
        try:
            self.host = host or self.os.environ['db_host']
            self.dbname = dbname or self.os.environ['db_name']
            self.user = user or self.os.environ['db_user']
            self.password = password or self.os.environ['db_password']
            self.port = port or self.os.environ['db_port']
        except:
            raise Excption('No database credentials found')

        self.conn, self.cursor = self.connect_to_postgres()

    def __enter__(self):
        return self

    def connect_to_postgres(self):
        for n in range(10):
            try:
                conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % \
                    (self.host, self.dbname, self.user, self.password, self.port)
                conn = self.psycopg2.connect(conn_string)
                cursor = conn.cursor()
                return conn, cursor
            except:
                self.time.sleep(5) # sleep for 5 seconds and try again

    def execute_query(self, query, has_results=True):
        # if connection closed then reconnect
        if self.conn.closed == 1:
            self.conn, self.cursor = self.connect_to_postgres()

        self.cursor.execute(query)

        if has_results:
            results = self.cursor.fetchall()
            self.rollback()

            return results
        else:
            self.conn.commit()
            self.rollback()

            return True

    def rollback(self):
        self.conn.rollback()

    def __exit__(self, type, value, traceback):
        self.conn.close()

if __name__ == '__main__':
    import os

    query = '''select * from schema.table limit 1;'''

    pg_helper = PGHelper(dbname=os.environ['db_name'],
                         host=os.environ['db_host'],
                         user=os.environ['db_user'],
                         password=os.environ['db_password'],
                         port=os.environ['db_port'])

    results = pg_helper.execute_query(query=query)

    with PGHelper() as pg_helper:
        results = pg_helper.execute_query(query=query)
