from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact = Table('contact', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('catagory', VARCHAR(length=32)),
    Column('value', VARCHAR(length=128)),
)

contact = Table('contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=32)),
    Column('text', String(length=128)),
    Column('_type', String(length=32)),
    Column('user_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=16)),
    Column('password', String(length=32)),
    Column('position', String(length=32)),
    Column('corp', String(length=32)),
    Column('name', String(length=32)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].columns['catagory'].drop()
    pre_meta.tables['contact'].columns['value'].drop()
    post_meta.tables['contact'].columns['_type'].create()
    post_meta.tables['contact'].columns['text'].create()
    post_meta.tables['contact'].columns['title'].create()
    post_meta.tables['contact'].columns['user_id'].create()
    post_meta.tables['user'].columns['corp'].create()
    post_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['position'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['contact'].columns['catagory'].create()
    pre_meta.tables['contact'].columns['value'].create()
    post_meta.tables['contact'].columns['_type'].drop()
    post_meta.tables['contact'].columns['text'].drop()
    post_meta.tables['contact'].columns['title'].drop()
    post_meta.tables['contact'].columns['user_id'].drop()
    post_meta.tables['user'].columns['corp'].drop()
    post_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['position'].drop()
