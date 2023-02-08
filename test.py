# # import prison
# # b = {
# #     "bool": True,
# #     "list": ["a", "b", "c"],
# #     "number": 777,
# #     "string": "string",
# #     "null": None
# # }

# # print(prison.dumps(b))

# >>> db.get_tables_for_bind()

# [
#     Table(
#         'ab_permission', MetaData(), 
#         Column('id', Integer(), table=<ab_permission>, 
#         primary_key=True, nullable=False, 
#         default=Sequence('ab_permission_id_seq', metadata=MetaData())), 
        
#         Column('name', String(length=100), table=<ab_permission>, nullable=False), schema=None
#         ), 
#     Table('ab_view_menu', MetaData(), Column('id', Integer(), table=<ab_view_menu>, primary_key=True, nullable=False, default=Sequence('ab_view_menu_id_seq', metadata=MetaData())), Column('name', String(length=250), table=<ab_view_menu>, nullable=False), schema=None), 
    
#     Table('ab_permission_view_role', MetaData(), Column('id', Integer(), table=<ab_permission_view_role>, primary_key=True, nullable=False, default=Sequence('ab_permission_view_role_id_seq', metadata=MetaData())), Column('permission_view_id', Integer(), ForeignKey('ab_permission_view.id'), table=<ab_permission_view_role>), Column('role_id', Integer(), ForeignKey('ab_role.id'), table=<ab_permission_view_role>), schema=None), 
    
#     Table('ab_role', MetaData(), Column('id', Integer(), table=<ab_role>, primary_key=True, nullable=False, default=Sequence('ab_role_id_seq', metadata=MetaData())), Column('name', String(length=64), table=<ab_role>, nullable=False), schema=None), 
    
#     Table('ab_permission_view', MetaData(), Column('id', Integer(), table=<ab_permission_view>, primary_key=True, nullable=False, default=Sequence('ab_permission_view_id_seq', metadata=MetaData())), Column('permission_id', Integer(), ForeignKey('ab_permission.id'), table=<ab_permission_view>), Column('view_menu_id', Integer(), ForeignKey('ab_view_menu.id'), table=<ab_permission_view>), schema=None), 
    
#     Table('ab_user_role', MetaData(), Column('id', Integer(), table=<ab_user_role>, primary_key=True, nullable=False, default=Sequence('ab_user_role_id_seq', metadata=MetaData())), Column('user_id', Integer(), ForeignKey('ab_user.id'), table=<ab_user_role>), Column('role_id', Integer(), ForeignKey('ab_role.id'), table=<ab_user_role>), schema=None), 
    
#     Table('ab_user', MetaData(), Column('id', Integer(), table=<ab_user>, primary_key=True, nullable=False, default=Sequence('ab_user_id_seq', metadata=MetaData())), Column('first_name', String(length=64), table=<ab_user>, nullable=False), Column('last_name', String(length=64), table=<ab_user>, nullable=False), Column('username', String(length=64), table=<ab_user>, nullable=False), Column('password', String(length=256), table=<ab_user>), Column('active', Boolean(), table=<ab_user>), Column('email', String(length=64), table=<ab_user>, nullable=False), Column('last_login', DateTime(), table=<ab_user>), Column('login_count', Integer(), table=<ab_user>), Column('fail_login_count', Integer(), table=<ab_user>), Column('created_on', DateTime(), table=<ab_user>, default=ColumnDefault(<function User.<lambda> at 0x7fa3a522d1f0>)), Column('changed_on', DateTime(), table=<ab_user>, default=ColumnDefault(<function User.<lambda> at 0x7fa3a522d310>)), Column('created_by_fk', Integer(), ForeignKey('ab_user.id'), table=<ab_user>, default=ColumnDefault(<function User.get_user_id at 0x7fa3a522d940>)), Column('changed_by_fk', Integer(), ForeignKey('ab_user.id'), table=<ab_user>, default=ColumnDefault(<function User.get_user_id at 0x7fa3a522dca0>)), schema=None), 
    
#     Table('ab_register_user', MetaData(), Column('id', Integer(), table=<ab_register_user>, primary_key=True, nullable=False, default=Sequence('ab_register_user_id_seq', metadata=MetaData())), Column('first_name', String(length=64), table=<ab_register_user>, nullable=False), Column('last_name', String(length=64), table=<ab_register_user>, nullable=False), Column('username', String(length=64), table=<ab_register_user>, nullable=False), Column('password', String(length=256), table=<ab_register_user>), Column('email', String(length=64), table=<ab_register_user>, nullable=False), Column('registration_date', DateTime(), table=<ab_register_user>, default=ColumnDefault(<function datetime.now at 0x7fa3a522d3a0>)), Column('registration_hash', String(length=256), table=<ab_register_user>), schema=None), 
    
    
    
#     Table('contact_group', MetaData(), Column('id', Integer(), table=<contact_group>, primary_key=True, nullable=False), Column('name', String(length=50), table=<contact_group>, nullable=False), schema=None), 
    
#     Table('gender', MetaData(), Column('id', Integer(), table=<gender>, primary_key=True, nullable=False), Column('gender', String(length=2), table=<gender>, nullable=False), schema=None), 
    
#     Table('contact', MetaData(), Column('id', Integer(), table=<contact>, primary_key=True, nullable=False), Column('name', String(length=150), table=<contact>, nullable=False), Column('address', String(length=564), table=<contact>, default=ColumnDefault('Street ')), Column('birthday', Date(), table=<contact>), Column('personal_phone', String(length=20), table=<contact>), Column('personal_cellphone', String(length=20), table=<contact>), Column('contact_group_id', Integer(), ForeignKey('contact_group.id'), table=<contact>), schema=None), 
    
#     Table('country', MetaData(), Column('id', Integer(), table=<country>, primary_key=True, nullable=False), Column('name', String(length=50), table=<country>, nullable=False), schema=None), 
    
#     Table('country_stats', MetaData(), Column('id', Integer(), table=<country_stats>, primary_key=True, nullable=False), Column('stat_date', Date(), table=<country_stats>), Column('population', Float(), table=<country_stats>), Column('unemployed_perc', Float(), table=<country_stats>), Column('poor_perc', Float(), table=<country_stats>), Column('college', Float(), table=<country_stats>), Column('country_id', Integer(), ForeignKey('country.id'), table=<country_stats>, nullable=False), schema=None)]

# >>> 

a = 4 

def polynomial(a, b, c, x):
    return a*x**2 + b*x + c

b = a
b *= a
c = 1
result = polynomial(a, b, c, 0)
a += 3
a = 0

print(a, b, c, result)