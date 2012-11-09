from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, func, and_
from sqlalchemy.orm import relationship
from sqlalchemy import and_

from firsttest.models import Base, DBSession

class EntryType(Base):
    __tablename__ = 'entry_types'

    id = Column(String(5), primary_key = True, nullable = False)
    description = Column(String(50), nullable = False)

class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key = True, nullable = False)
    date = Column(DateTime, nullable = False)
    title = Column(String(75), nullable = False)
    entry = Column(Text)
    entry_type = Column(String(2), ForeignKey('entry_types.id'), nullable = False)

    entry_type_detail = relationship("EntryType")

class GalleryPermission(Base):
    __tablename__ = 'gallery_permissions'
    gallery_id = Column(Integer, ForeignKey('galleries.id'), primary_key = True, nullable = False)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key = True, nullable = False)

    role = relationship('Role')

class Gallery(Base):
    __tablename__ = 'galleries'

    id = Column(Integer, primary_key = True, nullable = False)
    directory_name = Column(String(25))
    title = Column(String(200))
    description = Column(String(10000))
    created = Column(DateTime)
    creator = Column(Integer, ForeignKey('users.id'))
    modified= Column(DateTime)
    last_update_by = Column(Integer, ForeignKey('users.id'))
    gallery_date = Column(DateTime)

    media = relationship('Medium', backref = 'gallery')
    creator_detail = relationship('User', primaryjoin = 'User.id == Gallery.creator')
    permission = relationship('GalleryPermission', cascade = 'all,delete', backref = 'gallery')

    @classmethod
    def get(cls, gallery_id, user):
        gallery = DBSession.query(cls) \
                .join(GalleryPermission) \
                .filter(and_(
                cls.id == gallery_id,
                GalleryPermission.role_id.in_(user.role_ids))).first()
        return gallery

class Medium(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key = True, nullable = False)
    file_name = Column(String(200))
    title = Column(String(200))
    description = Column(String(10000))
    created = Column(DateTime)
    creator = Column(Integer)
    modified= Column(DateTime)
    last_update_by = Column(Integer)
    thumbnail_name = Column(String(200))
    media_type = Column(String(10), ForeignKey('media_types.id'))
    gallery_id = Column(Integer, ForeignKey('galleries.id'))

    media_class = relationship('MediumType')

    @classmethod
    def get(cls, medium_id, user):
        medium = DBSession.query(cls) \
                .join(Gallery, GalleryPermission) \
                .filter(and_(
                    cls.id == medium_id,
                    GalleryPermission.role_id.in_(user.role_ids))).first()
        return medium

class MediumType(Base):
    #faux constants
    IMAGE = 'IMAGE'

    __tablename__ = 'media_types'
    id = Column(Integer, primary_key = True, nullable = False)
    code = Column(String(10))
    description = Column(String(100))




