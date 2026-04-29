import urllib
from sqlalchemy import create_engine
from config import *

connection_string = (
    f"Driver={{{DB_DRIVER}}};"
    f"Server=tcp:{DB_SERVER},1433;"
    f"Database={DB_DATABASE};"
    f"Uid={DB_USERNAME};"
    f"Pwd={DB_PASSWORD};"
    "Encrypt=yes;"
)

params = urllib.parse.quote_plus(connection_string)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")