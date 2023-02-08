# from flask import flash
# from flask_appbuilder import SimpleFormView
# from flask_babel import lazy_gettext as _

# from flask_appbuilder import expose, has_access, AppBuilder, BaseView
# from app import appbuilder
# from formtest import MyForm

# class MyFormView(SimpleFormView):
#     form = MyForm
#     form_title = 'This is my first form view'
#     message = 'My form submitted'

#     @expose('/getform')
#     @has_access
#     def form_get(self, form):
#         form.field1.data = 'This was prefilled'

#     @expose('/postform')
#     @has_access
#     def form_post(self, form):
#         # post process form
#         flash(self.message, 'info')

# appbuilder.add_view(MyFormView, "My form View", icon="fa-group", label=_('My form View'),
#                      category="My Forms", category_icon="fa-cogs")

# appbuilder.add_link("Form", href='/forms/getform', category='My Forms')