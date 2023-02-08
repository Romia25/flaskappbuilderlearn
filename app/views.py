from .formtest import MyForm
from .models import *

from flask import render_template, request, redirect
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi, MultipleView, MasterDetailView, \
    CompactCRUDMixin
from flask_appbuilder import expose, BaseView, AppBuilder, has_access, action
from flask_appbuilder.models.sqla.filters import FilterStartsWith
from flask_appbuilder.api import BaseApi, rison, safe
from flask_appbuilder.security.decorators import protect
from app import appbuilder, db
from flask_appbuilder.charts.views import DirectByChartView, GroupByChartView, ChartView
from flask_appbuilder.models.group import aggregate_sum, aggregate_count, aggregate_avg
from flask_appbuilder.widgets import ListThumbnail

#from . import appbuilder, db

from flask import flash
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _

# MyForm

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )

#@appbuilder.app.add_template_global(f)
def footer():
    return (
        render_template(
            "footer.html", base_template=appbuilder.base_template, appbuilder=appbuilder
            )
        )

list_template = "footer.html"
appbuilder.base_template
    

db.create_all()

# From here it's my code lessons

class MyView(BaseView):

    default_view = 'method1'
    list_template = "footer.html"


    @expose('/method1/')
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return 'Hello'

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return param1
    
    @expose('/method3/<string:param1>')
    @has_access
    def method3(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('method3.html',
                            param1 = param1)


appbuilder.add_view(MyView, "Method1", category='My View')
appbuilder.add_link("Method2", href='/myview/method2/john', category='My View')
appbuilder.add_link("Method3", href='/myview/method3/Linda', category='My View')



class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'This is my first form view'
    message = 'My form submitted'

    @expose('/getform')
    @has_access
    def form_get(self, form):
        form.field1.data = 'This was prefilled'

    @expose('/postform')
    @has_access
    def form_post(self, form):
        # post process form
        flash(self.message, 'info')

appbuilder.add_view(MyFormView, "My form View", icon="fa-group", label=_('My form View by Line'),
                     category="My Forms", category_icon="fa-cogs")

appbuilder.add_link("Form", href='/myformview/getform', category='My Forms')
appbuilder.add_link("FormPost", href='/myformview/postform', category='My Forms')


#necessary for contacts app goes down there

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)


    label_columns = {'contact_group':'Contacts Group'}
    list_columns = ['name','personal_cellphone','birthday','contact_group']

    show_fieldsets = [
        (
            'Summary',
            {'fields': ['name', 'address', 'contact_group']}
        ),
        (
            'Personal Info',
            {'fields': ['birthday', 'personal_phone', 'personal_cellphone'], 'expanded': False}
        ),
    ]

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]
    list_template = "temptest.html"
    template = "footer.html"


    @action("myaction","Do something on this record","Do you really want to?","fa-rocket")
    def myaction(self, item):
        """
            do something with the item record
        """
        return redirect(self.get_redirect())
    
    @action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())

#add this class to see if you can create gender item
class GenderView(ModelView):
    datamodel = SQLAInterface(Gender)
    



appbuilder.add_view(
    GroupModelView,
    "List Groups",
    icon = "fa-folder-open-o",
    category = "Contacts",
    category_icon = "fa-envelope"
)
appbuilder.add_view(
    ContactModelView,
    "List Contacts",
    icon = "fa-envelope",
    category = "Contacts"
)


class MultipleViewsExp(MultipleView):
    views = [GroupModelView, ContactModelView]

appbuilder.add_view(
    MultipleViewsExp,
    "Multiple Views",
    icon="fa-envelope",
    category="Contacts"
)

class GroupMasterView(MasterDetailView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

appbuilder.add_view(
    GroupMasterView,
    "Master detailed Views",
    icon="fa-envelope",
    category="Contacts"
)

#restful api creation goes down there

class ExampleApi(BaseApi):

    #route_base = '/newapi/v2/nice'
    resource_name = 'example'

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            }
        }
    }

    apispec_parameter_schemas = {
        "greeting_schema": schema
    }

    @expose('/greeting')
    def greeting(self):
        """Send a greeting
        ---
        Get:
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        return self.response(200, message="Hello")
    
    @expose('/greeting2', methods=['POST', 'GET'])
    def greeting2(self):
        """Send a greeting
        ---
        Get:
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        post:
          responses:
            201:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        if request.method == 'GET':
            return self.response(200, message="Hello (GET)")
        return self.response(201, message="Hello (POST)")
    
    @expose('/greeting3')
    @rison()
    def greeting3(self, **kwargs):
        if 'name' in kwargs['rison']:
            return self.response(
                200,
                message=f"Hello {kwargs['rison']['name']}"
            )
        return self.response_400(message="Please send your name")
    
    @expose('/risonjson')
    @rison()
    def rison_json(self, **kwargs):
        return self.response(200, result=kwargs['rison'])
    



    @expose('/greeting4')
    @rison(schema)
    def greeting4(self, **kwargs):
        """Get item from Model
        ---
        Get:
          parameters:
          - $ref: '#/components/parameters/greeting_schema'
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                schema:
                  type: object
                  properties:
                    message:
                      type: string
        """
        return self.response(
            200,
            message=f"Hello {kwargs['rison']['name']}"
        )
    
    @expose('/error')
    @protect()
    @safe
    def error(self):
        """Error 500
        ---
        Get:
          responses:
            500:
              $ref: '#/components/responses/500'
        """
        raise Exception
    
    @expose('/private')
    @protect()
    def rison_json2(self):
        """Say it's risonjson2
        ---
        Get:
          responses:
            200:
              description: Say it's private
              content:
                application/json:
                  schema:
                    type: object
            401:
              $ref: '#/components/responses/401'        
        """
        return self.response(200, message="This is private")

appbuilder.add_api(ExampleApi)

class GroupModelApi(ModelRestApi):
    resource_name = 'group'
    datamodel = SQLAInterface(ContactGroup)

appbuilder.add_api(GroupModelApi)

class ContactModelApi(ModelRestApi):
    resource_name = 'contact'
    datamodel = SQLAInterface(Contact)
    add_query_rel_fields = {
        'gender': [['name', FilterStartsWith, 'F']]
    }

    order_rel_fields = {
        'contact_group': ('name', 'asc'),
        'gender': ('name', 'asc')
    }
    
    #get item of contact model
    show_columns = ['name', 'age']
    show_select_columns = ['name', 'birthday']
    show_columns = ['name', 'some_function']

# #charts views definition goes down there
# class CountryDirectChartView(DirectByChartView):
#     datamodel = SQLAInterface(CountryStats)
#     chart_title = 'Direct Data Example'

#     definitions = [
#         {
#             'label': 'Unemployment',
#             'group': 'stat_date',
#             'series': ['unemployed_perc',
#                     'college_perc']
#         },
#         {
#             'label': 'Poor',
#             'group': 'stat_date',
#             'series': ['poor_perc',
#                     'college_perc']
#         }
#     ]

# appbuilder.add_view(CountryDirectChartView, "Show Country Chart", icon="fa-dashboard", category="Statistics")

class CountryGroupByChartView(GroupByChartView):
    datamodel = SQLAInterface(CountryStats)
    related_views = [Country]
    chart_title = 'Statistics'

    definitions = [
        {
            'label': 'Country Stat',
            'group': 'country',
            'series': [(aggregate_avg, 'unemployed_perc'),
                       (aggregate_avg, 'population'),
                       (aggregate_avg, 'college_perc')
                      ]
        }
    ]

appbuilder.add_view(CountryGroupByChartView, "Show Country Chart", icon="fa-dashboard", category="Statistics")

class ContactChartView(ChartView):
    search_columns = ['name','contact_group']
    datamodel = SQLAInterface(Contact)
    chart_title = 'Grouped contacts'
    label_columns = ContactModelView.label_columns
    group_by_columns = ['contact_group']

appbuilder.add_view(ContactChartView, "Contacts charts", category="Contacts")

class PersonModelView(ModelView):
    datamodel = SQLAInterface(Person)

    list_widget = ListThumbnail

    label_columns = {'name':'Name','photo':'Photo','photo_img':'Photo', 'photo_img_thumbnail':'Photo Thumb'}
    list_columns = ['photo_img_thumbnail', 'name', 'photo_img']
    show_columns = ['photo_img','name']

    show_fieldsets = [
        ("Summary", {"fields": ["photo_img", "name"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "name",
                    "photo_img"
                ],
                "expanded": False,
            },
        ),
        ("Extra", {"fields": ["notes"], "expanded": False}),
    ]

    # add_fieldsets = [
    #     ("Summary", {"fields": ["name", "photo", "address", "person_group"]}),
    #     (
    #         "Personal Info",
    #         {
    #             "fields": [
    #                 "birthday",
    #                 "personal_phone",
    #                 "personal_celphone",
    #                 "personal_email",
    #             ],
    #             "expanded": False,
    #         },
    #     ),
    #     (
    #         "Professional Info",
    #         {
    #             "fields": [
    #                 "business_function",
    #                 "business_phone",
    #                 "business_celphone",
    #                 "business_email",
    #             ],
    #             "expanded": False,
    #         },
    #     ),
    #     ("Extra", {"fields": ["notes"], "expanded": False}),
    # ]

    # edit_fieldsets = [
    #     ("Summary", {"fields": ["name", "photo", "address", "person_group"]}),
    #     (
    #         "Personal Info",
    #         {
    #             "fields": [
    #                 "birthday",
    #                 "personal_phone",
    #                 "personal_celphone",
    #                 "personal_email",
    #             ],
    #             "expanded": False,
    #         },
    #     ),
    #     (
    #         "Professional Info",
    #         {
    #             "fields": [
    #                 "business_function",
    #                 "business_phone",
    #                 "business_celphone",
    #                 "business_email",
    #             ],
    #             "expanded": False,
    #         },
    #     ),
    #     ("Extra", {"fields": ["notes"], "expanded": False}),
    # ]


appbuilder.add_view(PersonModelView, "Try upload images", category="Contacts")

#Down there goes modelview for file upload
class ProjectFilesModelView(ModelView):
    datamodel = SQLAInterface(ProjectFiles)

    label_columns = {"file_name": "File Name", "download": "Download"}
    add_columns = ["file", "description", "project"]
    edit_columns = ["file", "description", "project"]
    list_columns = ["file_name", "download"]
    show_columns = ["file_name", "download"]


class ProjectModelView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(Project)
    related_views = [ProjectFilesModelView]

    show_template = "appbuilder/general/model/show_cascade.html"
    edit_template = "appbuilder/general/model/edit_cascade.html"

    add_columns = ["name"]
    edit_columns = ["name"]
    list_columns = ["name", "created_by", "created_on", "changed_by", "changed_on"]
    show_fieldsets = [
        ("Info", {"fields": ["name"]}),
        (
            "Audit",
            {
                "fields": ["created_by", "created_on", "changed_by", "changed_on"],
                "expanded": False,
            },
        ),
    ]



appbuilder.add_view(
    ProjectModelView, "List Projects", icon="fa-table", category="Projects"
)
appbuilder.add_view_no_menu(ProjectFilesModelView)

#Here goes modelview definition for manay to many with extra property
#this lines of code are place here beacause we use this modelview definition in employeeview
class EmployeeHistoryView(ModelView):
    datamodel = SQLAInterface(EmployeeHistory)
    list_columns = ['department', 'begin_date', 'end_date']

#One to many relationship modelview example
class EmployeeView(ModelView):
    datamodel = SQLAInterface(Employee)

    list_columns = ['full_name', 'department', 'employee_number']

    #we add this for many to many with extra property
    related_views = [EmployeeHistoryView]
    show_template = 'appbuilder/general/model/show_cascade.html'


class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)
    related_views = [EmployeeView]


class DepartmentView(ModelView):
    datamodel = SQLAInterface(Department)
    related_views = [EmployeeView]


appbuilder.add_view(EmployeeView, "Employees", icon="fa-folder-open-o", category="Company")
appbuilder.add_separator("Company")
appbuilder.add_view(DepartmentView, "Departments", icon="fa-folder-open-o", category="Company")
appbuilder.add_view(FunctionView, "Functions", icon="fa-folder-open-o", category="Company")


#Here goes the modelview definition for the many to many relationship
class BenefitView(ModelView):
    datamodel = SQLAInterface(Benefit)
    related_views = [EmployeeView]
    add_columns = ['name']
    edit_columns = ['name']
    show_columns = ['name']
    list_columns = ['name']

appbuilder.add_view(BenefitView, "Benefits", icon="fa-folder-open-o", category="Company")

appbuilder.add_view_no_menu(EmployeeHistoryView, "EmployeeHistoryView")