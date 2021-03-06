import python_path

from ml_workflow.data_source import DataSource
from ml_workflow.session import Session
import sqlite3

import utils
from ml_workflow.workflow_node import WorkflowNode
import ml_workflow
import pandas as pd
import numpy as np
import os
import json
import datetime as dt

TEMP_DB_NAME = 'temp_for_test.db'


def set_up_fake_db():
    if os.path.isfile(TEMP_DB_NAME):
        os.remove(TEMP_DB_NAME)

    conn = sqlite3.connect(TEMP_DB_NAME)
    conn.execute('CREATE TABLE fake(id INTEGER);')
    conn.execute('INSERT INTO fake(id) VALUES(1), (4), (9), (16), (25);')
    conn.commit()

    return conn


@DataSource(name='Exemple_simple_query', source_type='db',
            source='fake', frozen_ignore_args=['conn'])
def get_simple_query_results(conn, orig=0):
    return conn.execute('SELECT * FROM fake').fetchall()[orig:]


def clean_db(conn):
    conn.execute('DELETE FROM fake;')
    conn.commit()

def as_json(data):
    return json.loads(json.dumps(data))

def test_frozen_session():
    conn = set_up_fake_db()

    res_1 = get_simple_query_results(conn)
    res_5 = get_simple_query_results(conn, 1)

    with Session.record_data_source('temp/test_session_record'):
        res_2 = get_simple_query_results(conn)
        res_4 = get_simple_query_results(conn, 1)

    assert(res_1 == res_2)
    assert(res_4 == res_5)

    clean_db(conn)

    assert(get_simple_query_results(conn) == [])

    with Session.play_data_source_record('temp/test_session_record'):
        res_1_recorded = get_simple_query_results(conn)
        res_5_recorded = get_simple_query_results(conn, 1)

    assert(as_json(res_1) == res_1_recorded)
    assert(as_json(res_5) == res_5_recorded)

    with Session.record_data_source('temp/test_session_record'):
        assert(get_simple_query_results(conn) == [])

    with Session.play_data_source_record('temp/test_session_record'):
        assert(get_simple_query_results(conn) == [])

@DataSource(name='pd_returning_stuff')
def data_source_with_pd():
    return pd.DataFrame({'datetime' : [dt.datetime.now()]})

def test_frozen_session_with_df():
    with Session.record_data_source('temp/test_session_record_df'):
        df = data_source_with_pd()

    with Session.play_data_source_record('temp/test_session_record_df'):
        df2 = data_source_with_pd()

    assert(df.equals(df2))
