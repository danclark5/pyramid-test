from pyramid.view import view_config, forbidden_view_config
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from firsttest.lib.base import BaseView
from firsttest.models import User
import hashlib


class AuthViews(BaseView):

    @view_config(route_name='login', renderer='login/login.mako')
    @forbidden_view_config(renderer='login/login.mako')
    def login(self):
        request = self.request
        login_url = request.resource_url(request.context, 'login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/' # never use the login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = login = password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            if User.user_validate(login, password):
               headers = remember(request, login)
               return HTTPFound(location=came_from,
                       headers=headers)
            request.session.flash('Login failed')
            message = 'Failed login'
            print message

        return dict(
            page_title="Login",
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
            logged_in=authenticated_userid(request)
            )

    @view_config(route_name='logout')
    def logout(self):
        headers = forget(self.request)
        self.request.session.flash('You are now logged out')
        return HTTPFound(location = self.request.route_url('home'),
                headers = headers)
