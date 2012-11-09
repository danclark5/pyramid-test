from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import Allow, Everyone

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from auth import User, Role, user_check, get_user
from content import Entry, EntryType, Gallery, Medium, MediumType, GalleryPermission

#Temporary I hope
class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String(75), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class RootFactory(object):
    __name__ = ''
    __acl__ = [(Allow, Everyone, 'view'),
            (Allow, 'FAMILY', 'family'),
            (Allow, 'FRIENDS', 'friends'),
            (Allow, 'OWNER', 'owner'),
            (Allow, 'VISITORS', 'vistors'),
            (Allow, 'GALLERY_ADMIN', 'gallery_admin')]

    def __init__(self, request):
        pass
