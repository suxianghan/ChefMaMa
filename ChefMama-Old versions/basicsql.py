import sqlalchemy 
from sqlalchemy import (Table, Column, Integer, String, Float, Date,
                        MetaData, create_engine)
from sqlalchemy.sql import select
from datetime import date



engine = create_engine('sqlite:///test.db')#change url when we actually have a database

metadata = MetaData()

users = sqlalchemy.Table('user', metadata,
	Column('username', String(100), primary_key=True),
    Column('password', String(20)),
    Column('email', String(100)))
query=users.create(engine, checkfirst=True)	

insert_query=users.insert().values(username="Tonys2",password="123456",email="filler@gmail.com")

# The Query we will execute
print insert_query.compile()
# The parameters to this query
print insert_query.compile().params


# Actually run the query
connection = engine.connect()
#connection.execute(insert_query)

# Run some more insertions
"""connection.execute(users.insert(), [
   	    {'username': 'abc1', 'password': 'john', 'email': 'doe'},
       	{'username': 'def2', 'password': 'jane', 'email': 'doe'}
   	])"""

# Simple "SELECT"
def get_users():	
	retlist=[]
	s = select([users]) # Equivilant to "SELECT * FROM students"
	result = connection.execute(s)
	for i in result:
		retlist.append(i)
	return retlist

#parametrized select
def user_search(user):
	s = select([users.c.username]).where(users.c.username == user)
	for i in connection.execute(s):
		print i

def add_user(name,passw,em):
	connection.execute(users.insert(),[{'username':name,"password":passw,'email':em}])


print(get_users())
#add_user('mammamia','pizzeria','mama@pizza.com')
print(get_users())