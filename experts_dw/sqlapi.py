from . import db
import os
import pugsql

sqlapi = pugsql.module(os.path.dirname(os.path.abspath(__file__)) + '/sql/')
sqlapi.set_engine(db.engine('hotel'))
