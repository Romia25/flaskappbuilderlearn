from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text, Table
from sqlalchemy.orm import relationship

from flask_appbuilder.models.mixins import ImageColumn, AuditMixin, FileColumn

from flask import url_for, Markup
from flask_appbuilder.filemanager import ImageManager, get_file_original_name

import datetime

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name

class Gender(Model):
    id = Column(Integer, primary_key=True)
    gender = Column(String(2), unique = True, nullable = True)




class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address =  Column(String(564), default='Street ')
    birthday = Column(Date)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'))
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey('gender.id'))
    gender = relationship("Gender")

    def __repr__(self):
        return self.name
    
    #@property is usued to render transformed outpout
    @property
    def age(self):
        return Date.today().year - self.birthday.year
    
    def some_function(self):
        return f"Hello {self.name}"

#chart view model start here
class Country(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name
    

class CountryStats(Model):
    id = Column(Integer, primary_key=True)
    stat_date = Column(Date, nullable=True)
    population = Column(Float)
    unemployed_perc = Column(Float)
    poor_perc = Column(Float)
    college = Column(Float)
    #country_id = Column(Integer, ForeignKey('country.id'), nullable=True)
    #country = relationship("Country")

    def college_perc(self):
        if self.population != 0:
            return (self.college*100)/self.population
        else:
            return 0.0
    
    def month_year(self):
        return datetime.datetime(self.stat_date.year, self.stat_date.month, 1)

#image and file managing goes down there
class Person(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique = True, nullable=False)
    photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(self.photo) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url_thumbnail(self.photo) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')


#Down there goes model definition for file upload
class Project(AuditMixin, Model):
    __tablename__ = "project"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)


class ProjectFiles(Model):
    __tablename__ = "project_files"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    project = relationship("Project")
    file = Column(FileColumn, nullable=False)
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("ProjectFilesModelView.download", filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

#One to many relationship model definition example
class Department(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Function(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


def today():
    return datetime.datetime.today().strftime('%Y-%m-%d')

#Down there goes model definition for many to many relationship
#notes that the employee model is part of one to many relationship too
#you just have to remove code for benefit's model and all reference to it

class Benefit(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

assoc_benefits_employee = Table('benefits_employee', Model.metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('benefit_id', Integer, ForeignKey('benefit.id')),
                                      Column('employee_id', Integer, ForeignKey('employee.id'))
)


class Employee(Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    address = Column(Text(250), nullable=False)
    fiscal_number = Column(Integer, nullable=False)
    employee_number = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    function_id = Column(Integer, ForeignKey('function.id'), nullable=False)
    function = relationship("Function")
    #here goes the reference to benifit model (many to many relationship)
    benefits = relationship('Benefit', secondary=assoc_benefits_employee, backref='employee')
    #
    begin_date = Column(Date, default=today, nullable=False)
    end_date = Column(Date, nullable=True)

    def __repr__(self):
        return self.full_name


#Here goes many to many relationship with extra property model definition
class EmployeeHistory(Model):
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department = relationship("Department")
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    employee = relationship("Employee")
    begin_date = Column(Date, default=today)
    end_date = Column(Date)
