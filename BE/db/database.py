import sqlalchemy
from databases import Database
import pandas as pd




user = 'root'
password = 'pass'
host = '127.0.0.1'
port = '3306'
dbname = 'CELDE'
DATABASE_URL = "mysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port,dbname)
database = Database(DATABASE_URL)

sqlalchemy_engine = sqlalchemy.create_engine(url=DATABASE_URL)


# engine.execute("CREATE DATABASE dbname") #create db
# engine.execute("USE dbname")

def get_database() -> Database:
    return database

