import sqlite3
import pandas as pd
import random

pcr_tests_db = 'data/pcr_tests.db'
consultation_db = 'data/consultations.db'

def create_table_and_db_pcr_test():
    conn = sqlite3.connect(pcr_tests_db)

    conn.execute("DROP TABLE IF EXISTS pcr_test;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pcr_test (
            id int PRIMARY KEY,
            person_id int,
            pcr_result varchar(32) NOT NULL,
            test_date date NOT NULL
        );
    """)

    return conn

def generate_pcr_tests():
    df = pd.read_csv('data/train.csv')
    people_id = df['id']

    min_id, max_id = people_id.min(), people_id.max()

    conn = create_table_and_db_pcr_test()

    for it in range(people_id.min(), people_id.max() + 1):
        conn.execute(
            "INSERT INTO pcr_test(id, person_id, pcr_result, test_date) VALUES(?, ?, ?, date('2020-03-01', '+{i} day'));".format(
                i = random.randint(1, 120)
                ),
            (it, it, 'positive' if random.random() < 0.5 else 'negative')
        )

    conn.commit()

def create_consultations_table():
    conn = sqlite3.connect(consultation_db)

    conn.execute("DROP TABLE IF EXISTS consultations;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id int PRIMARY KEY,
            person_id int,
            services varchar(32) NOT NULL,
            hospital varchar(32) NOT NULL,
            consultation_date date NOT NULL
        );
    """)

    return conn

def generate_consultations():
    conn = create_consultations_table()

    df = pd.read_csv('data/train.csv')
    people_id = df['id']

    min_id, max_id = people_id.min(), people_id.max()

    for it in range(2*len(df)):
        conn.execute(
            "INSERT INTO consultations(id, person_id, services, hospital, consultation_date) VALUES(?, ?, ?, ?, date('2020-03-01', '+{i} day'));".format(
                i = random.randint(1, 120)
                ),
            (
                it, 
                random.randint(min_id, max_id),
                random.choice(['SSR', 'HC', 'REA']),
                random.choice(['HEGP', 'Necker', 'Bichat', 'Pitié'])
            )
        )

    conn.commit()   

if __name__ == '__main__':
    generate_pcr_tests()
    generate_consultations()
    

