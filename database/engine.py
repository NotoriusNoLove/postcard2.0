import psycopg2.extras
from config import *

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=HOST,
    port=PORT
)
cur = conn.cursor()
