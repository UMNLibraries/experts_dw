from . import db
import os
import pugsql

sqlapi = pugsql.module(os.path.dirname(os.path.abspath(__file__)) + '/sql/')
sqlapi.setengine(db.engine('hotel'))
