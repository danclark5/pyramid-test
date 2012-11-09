from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid.events import BeforeRender
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from firsttest.models import DBSession, user_check, get_user
from firsttest.lib.subscribers import add_renderer_globals
import firsttest.views

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=user_check)
    authz_policy = ACLAuthorizationPolicy()
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings, root_factory = 'firsttest.models.RootFactory',
            session_factory=session_factory)
    config.add_subscriber(add_renderer_globals, BeforeRender)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_request_property(get_user, 'user', reify=True)
    config.add_static_view('static', 'static')
    config.add_route('priv_res', 'priv_res/*subpath')
    #config.add_view('firsttest.private_static.private_static_view', route_name='priv_res', permission='owner')
    config.add_route('home', '/')
    config.add_route('about', 'about')
    config.add_route('login', 'login')
    config.add_route('logout', 'logout')
    config.add_route('entry_index', 'entry/index')
    config.add_route('entry_view', 'entry/view/{id}')
    config.add_route('entry_edit', 'entry/edit/{id}')
    config.add_route('entry_new', 'entry/new')
    config.add_route('entry_delete', 'entry/delete')
    config.add_route('gallery_index', 'gallery/index')
    config.add_route('gallery_new', 'gallery/new')
    config.add_route('gallery_view', 'gallery/view/{id}')
    config.add_route('gallery_edit', 'gallery/edit/{id}')
    config.add_route('gallery_delete', 'gallery/delete')
    config.add_route('gallery_rebuild_symlinks', 'gallery/rebuild_symlinks')
    config.add_route('media_upload', 'media/upload')
    config.add_route('media_update_ajax', 'media/update_ajax')
    config.add_route('media_delete', 'media/delete')
    config.add_route('media_rotate', 'media/rotate/{medium_id}')
    config.add_route('media_restore', 'media/restore/{medium_id}')
    config.add_route('media_view', 'media/{medium_id}/{type}')
    config.scan()
    return config.make_wsgi_app()

