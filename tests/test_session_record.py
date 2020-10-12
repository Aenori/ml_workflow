import sqlite3

from common_import import *

from ml_workflow.data_source import mlwf_data_source

TEMP_DB_NAME = 'temp_for_test.db'

def set_up_fake_db():
    if os.path.isfile(TEMP_DB_NAME):
        os.remove(TEMP_DB_NAME)

    conn = sqlite3.connect(TEMP_DB_NAME)
    conn.execute('CREATE TABLE fake(id INTEGER);')
    conn.execute('INSERT INTO fake(id) VALUES(1), (4), (9), (16), (25);')
    conn.commit()

    return conn

@mlwf_data_source(name='Exemple_simple_query', frozen_ignore_args=[0])
def get_simple_query_results(conn, orig = 0):
    pass

def test_frozen_session():
    conn = set_up_fake_db()

