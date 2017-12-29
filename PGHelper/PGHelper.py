class PGHelper():
    import time
    import psycopg2
    from psycopg2 import extras, extensions
    import os

    def __init__(self, host=False, dbname=False, user=False, password=False, port=False, cursor_name=False):
        # this will allow you to <control + c> during a long running query
        self.extensions.set_wait_callback(self.extras.wait_select)

        try:
            self.host = host or self.os.environ['db_host']
            self.dbname = dbname or self.os.environ['db_name']
            self.user = user or self.os.environ['db_user']
            self.password = password or self.os.environ['db_password']
            self.port = port or self.os.environ['db_port']
        except:
            raise Excption('No database credentials found')

        self.cursor_name = cursor_name

        self.conn, self.cursor = self.connect_to_postgres()

    def __enter__(self):
        return self

    def add_cursor_name(self, cursor_name):
        self.cursor_name = cursor_name
        self.conn.close()
        self.conn, self.cursor = self.connect_to_postgres()

    def connect_to_postgres(self):
        for n in range(10):
            try:
                conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % \
                    (self.host, self.dbname, self.user, self.password, self.port)
                conn = self.psycopg2.connect(conn_string)
                if self.cursor_name:
                    cursor = conn.cursor(self.cursor_name)
                else:
                    cursor = conn.cursor()
                return conn, cursor
            except:
                self.time.sleep(5) # sleep for 5 seconds and try again

        raise Exception ('ALERT!! Unable to connect to Postgres')

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

    def iter_query(self, query):
        if self.cursor_name:
            self.cursor.execute(query)
            for record in self.cursor:
                yield record
        else:
            raise Exception('Must be using a named cursor. When you create the obj add the "cursor_name" parameter.')

    def rollback(self):
        self.conn.rollback()

    def __exit__(self, type, value, traceback):
        self.conn.close()

if __name__ == '__main__':
    import os
    from PGHelper import PGHelper
    
    pg_helper = PGHelper(dbname=os.environ['db_name'],
                         host=os.environ['db_host'],
                         user=os.environ['db_user'],
                         password=os.environ['db_password'],
                         port=os.environ['db_port'])

    results = pg_helper.execute_query(query='''select * from schema.table limit 1;''')
    "select pg_sleep(20)"

    # ------------------------
    import os
    from PGHelper import PGHelper

    with PGHelper(dbname=os.environ['db_name'],
                     host=os.environ['db_host'],
                     user=os.environ['db_user'],
                     password=os.environ['db_password'],
                     port=os.environ['db_port']) as pg_helper:
        results = pg_helper.execute_query(query='''select * from schema.table limit 1;''')

    # ------------------------
    from PGHelper import PGHelper
    from guppy import hpy
    h = hpy()
    start = h.heap().size

    with PGHelper(cursor_name='stream') as pg_helper:
        results = pg_helper.execute_query(query='''select * from schema.table limit 10000;''')

    finish = h.heap().size
    print ''
    print finish - start, 'bytes'
    # >> 5,320,864 bytes

    # ------------------------
    from PGHelper import PGHelper
    from guppy import hpy
    h = hpy()
    start = h.heap().size

    with PGHelper(cursor_name='stream') as pg_helper:
        query = '''select * from schema.table limit 10000;'''
        for record in pg_helper.iter_query(query):
            print record[0]
    finish = h.heap().size
    print ''
    print finish - start, 'bytes'
    # >> 8,000 bytes

    # ------------------------
    from PGHelper import PGHelper
    from guppy import hpy
    h = hpy()
    start = h.heap().size

    with PGHelper() as pg_helper:
        pg_helper.add_cursor_name(cursor_name='stream')
        query = '''select * from schema.table limit 10000;'''
        for record in pg_helper.iter_query(query=query):
            print record[0]
    finish = h.heap().size
    print ''
    print finish - start, 'bytes'
    # >> 7,992 bytes
