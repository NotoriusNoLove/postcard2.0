from .engine import *
from datetime import date, timedelta


def create_table() -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS people (
        name VARCHAR(255),
        group_id VARCHAR(50),
        birthday date);

        CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        group_id VARCHAR(50),
        text_birth VARCHAR(600),
        send_date date,
        image_path VARCHAR(255),
        submit boolean default true
        );

        CREATE TABLE IF NOT EXISTS groups(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        group_id VARCHAR(255)
        );
    """)
    conn.commit()


def insert_task(name, group_id, text_birth, send_date, image_path):
    query = """
        INSERT INTO tasks (name, group_id, text_birth, send_date, image_path) 
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (name, group_id, text_birth, send_date, image_path)

    cur.execute(query, values)
    conn.commit()

    cur.execute(f"""
        SELECT id
        FROM tasks
            WHERE name = '{name}'
        """)
    result = cur.fetchone()
    return result


def insert_users() -> None:
    cur.execute("SELECT * FROM people")
    result = cur.fetchall()
    if len(result) == 0:
        with open(r"storage\core\bir.csv", "r", encoding="utf-8") as df:
            cur.copy_from(df, "people", sep=';')
        conn.commit()


def get_users_birthday() -> list:
    # Вычисляем завтрашнюю дату
    tomorrow = (date.today() + timedelta(days=1)).strftime('%m-%d')

    # SQL-запрос с условием на завтрашнюю дату без учета года
    sql_query = """
    SELECT * FROM people 
    WHERE 
        EXTRACT(MONTH FROM birthday) = %s AND EXTRACT(DAY FROM birthday) = %s;"""

    cur.execute(sql_query, (tomorrow.split('-')[0], tomorrow.split('-')[1]))

    results = cur.fetchall()

    return results


def get_user_submit_true():
    cur.execute(f"""
    SELECT * FROM TASKS
    WHERE TO_CHAR(send_date, 'MM-DD') = '{(date.today()).strftime('%m-%d')}';
    """)
    result = cur.fetchall()
    return result


def get_chat_id(name):
    cur.execute(f"""
    SELECT group_id
        FROM groups
        WHERE name = '{name}'
    """)
    result = cur.fetchone()
    return result[0]
