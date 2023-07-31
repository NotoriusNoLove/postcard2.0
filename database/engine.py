import psycopg2.extras


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host='127.0.0.1',
    port='5432'
)
cur = conn.cursor()
