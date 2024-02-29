import os
from sqlalchemy import create_engine
import urllib



class Config():
  SECRET_KEY: str = 'secret'
  SECRET_COOKIE: str = 'secret'



class DevConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://root:root@127.0.0.1:3306/prueba'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
