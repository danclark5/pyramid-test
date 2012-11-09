from sqlalchemy import Column, Integer, Text, String, ForeignKey, func, and_
from sqlalchemy.orm import relationship

from pyramid.security import unauthenticated_userid

from firsttest.models import Base, DBSession

class Role(Base):
    __tablename__ = 'roles'

    OWNER = 1
    FAMILY = 2
    FRIENDS = 3
    VISTORS = 4
    GALLERY_VIEWER = 5
    GALLERY_ADMIN = 6

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(250))

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)

class User(Base):
    __tablename__ = 'users'

    VISITOR = 'vistor'

    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    password = Column(String(50))

    roles = relationship('Role', secondary=UserRole.__table__)

    @property
    def role_ids(self):
        '''Get the role_id associated with the user.'''
        return [role.id for role in self.roles]

    @classmethod
    def user_validate(cls, user, password):
        return DBSession.query(cls).filter(and_(cls.user == user,
            cls.password == func.password(password))).first()

    def check_role(self, role):
        return role in [(role.id) for role in self.roles]


def user_check(user, request):
    '''callback for the authentication policy'''
    user = DBSession.query(User).filter(User.user == user,
        ).first()
    return [(role.name) for role in user.roles] if user else None

def get_user(request):
    '''fetches the user. Used to attach a user object to the request'''
    user = unauthenticated_userid(request)
    if user is not None:
        return DBSession.query(User).filter(User.user == user).first()
    else:
        return DBSession.query(User).filter(User.user == User.VISITOR).first()
