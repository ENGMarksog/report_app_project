from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""
import psycopg2

conn = psycopg2.connect(database= "report_data_db",
                        user = "postgres",
                        password= "DatabasePassword",
                        host = "database-2.c82hez3678s7.us-east-2.rds.amazonaws.com",
                        port = "5432")

cursor = conn.cursor()
print(type(conn))
conn.close()

"""
