from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid, effective_principals

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc

from firsttest.models import DBSession, Entry, Role 


@view_config(route_name='home', renderer='home.mako')
def home(request):

    entry_level = ['NP']
    if request.user and (request.user.check_role(Role.FAMILY) 
            or request.user.check_role(Role.FRIENDS)):
        entry_level.append('RT')
    if request.user and request.user.check_role(Role.OWNER):
        entry_level.append('PS')
    entries = DBSession.query(Entry)\
            .filter(Entry.entry_type.in_(entry_level))\
            .order_by(desc(Entry.date)).limit(4).all()
    return {'entries':entries}

@view_config(route_name='about', renderer='about.mako')
def about(request):
    return {}
