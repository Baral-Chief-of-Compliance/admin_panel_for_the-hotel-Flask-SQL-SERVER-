from dotenv import load_dotenv
import os


load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = 'DESKTOP-CBFF35S\SQLEXPRESS'
    DATABASE = 'РГР_ГЛЕБ'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    DATABASE_CON = f'mssql://@{SERVER}/{DATABASE}?driver={DRIVER}'