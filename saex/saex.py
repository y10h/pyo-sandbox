#!/usr/bin/env python

import sqlalchemy as sa
import sqlalchemy.orm as orm

# describe tables
meta = sa.MetaData()

users = sa.Table('users', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.Unicode(120)),
)

credentials = sa.Table('credentials', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('login', sa.Unicode(10)),
    sa.Column('password', sa.Unicode(10)),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
)

# mapping classes
class User(object):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<User %r>" % self.name
    
    def __unicode__(self):
        return self.name

class Cred(object):

    def __repr__(self):
        return "<Cred (login %r) for %r>" % (self.login, self.user)

# mappers configuration
Session = orm.scoped_session(orm.sessionmaker())

Session.mapper(User, users)
Session.mapper(Cred, credentials, properties={
    'user': orm.relation(User, backref='creds'),
})

# setup engine
engine = sa.create_engine('sqlite:///')
meta.bind = engine
Session.configure(bind = engine)

# create schema and fill initial data
meta.create_all()

for user in [(1, u'Donald Duck'), 
             (2, u'Flash Gordon'),
             (3, u'John Doe')]:
    users.insert(user).execute()
del user
for cred in [(1, u'admin', u'moo', 1),
             (2, u'dduck', u'iam', 1),
             (3, u'fg',    u'bee', 2),
             (4, u'jo',    u'zip', 3)]:
    credentials.insert(cred).execute()
del cred

# inject IPython
from IPython.Shell import IPShellEmbed
shell = IPShellEmbed()
shell()
