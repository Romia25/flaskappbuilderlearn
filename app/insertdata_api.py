from .models import *

from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelRestApi
from app import appbuilder

class CountryModelApi(ModelRestApi):
    datamodel = SQLAInterface(Country)

appbuilder.add_api(CountryModelApi)

class GenderModelApi(ModelRestApi):
    datamodel = SQLAInterface(Gender)

appbuilder.add_api(GenderModelApi)

class ContactApi(ModelRestApi):
    datamodel = SQLAInterface(Contact)

appbuilder.add_api(ContactApi)
