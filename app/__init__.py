import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.menu import Menu

# down there goes necessary configuration for swagger integration (at least one tries)

# from flask_swagger_ui import get_swaggerui_blueprint

# bellow import will be used for dealing with migration
from flask_migrate import Migrate

# bellow import is used for naming configuration. It is used in migration dealing
from sqlalchemy import MetaData

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

#you add this to get what is wrong with swagger config
#logging.getLogger().setLevel(logging.ERROR)

# ///dealing with migration, you encounter an error because of constraint name
# it is possible to fix it by adding the constraint name in place of None in the
# [...]_initial_migration_test_by_line file in line 23 and 41.
# but dealing so, you will always have to do it manually. So you decided to use naming 
# convention to handle it generally. Bellow is a piece of it

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(referred_table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s"
}


app = Flask(__name__)
app.config.from_object("config")

# this is for metada initialisation. it is used in migration to 
# create name for constraint or indexes....
metadat = MetaData(naming_convention=convention)

# we add the parameter metadata and its argument metadat to the initialisation
# while we're dealing with migrations (constraint must have name... error)
db = SQLA(app, metadata=metadat)

# the following line is the initialization on a Migrate element
migrate = Migrate(app, db)

appbuilder = AppBuilder(app, db.session)

#Add this to see if swagger will work at least


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import views, insertdata_api
