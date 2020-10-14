import sqlite3
import pandas as pd


pcr_tests_db = 'data/pcr_tests.db'
consultation_db = 'data/consultations.db'

create_table_and_db_pcr_test(
    conn = sqlite3.connect(DB_FILE_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS passenger_hair_color (
            id int PRIMARY KEY,
            pcr_result varchar(32) NOT NULL,
            date
        );
    """)

    )

create_table_and_db_visites()


def generate_pcr_tests():
    df = pd.read_csv('train.csv')
    people_id = df['Id']

    min_id, max_id = people_id.min(), people_id.max()

    create_table_and_db_pcr_test()

    for it in range(len(people_id)*5//4):


    

