from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from firsttest.lib.base import BaseView
from firsttest.lib.forms import GallerySchema
from firsttest.models import DBSession, Gallery, Medium, User, GalleryPermission, Role
import random, string
from os import path, mkdir, rmdir
import os
import shutil
from datetime import datetime, date

class GalleryViews(BaseView):

    orderings = {'created' : Gallery.created,
            'title' : Gallery.title,
            'creator' : User.user,
            'medium_created' : Medium.created,
            'gallery_date' : Gallery.gallery_date}

    def __filter__(self, query):
        self.filter_errors = {}

        title = self.request.GET.get('title', None)
        if title:
            title = '%' + title.replace(' ', '%') + '%'
            query = query.filter(Gallery.title.like(title))

        date_kw = lambda x: ((x+'_date_'+i) for i in ['year', 'month', 'day'])
        start_date = None
        end_date = None
        if all((self.request.GET.get(x, None) for x in date_kw('start'))):
            try:
                start_date = date(*(int(self.request.GET[x]) for x in date_kw('start'))) 
            except ValueError as error:
                self.filter_errors['start_date'] = error.message.capitalize()
        elif any((self.request.GET.get(x, None) for x in date_kw('start'))):
            self.filter_errors['start_date'] = 'Incomplete date'
        if all((self.request.GET.get(x, None) for x in date_kw('end'))):
            try:
                end_date = date(*(int(self.request.GET[x]) for x in date_kw('end')))
            except ValueError as error:
                self.filter_errors['end_date'] = error.message.capitalize()
        elif any((self.request.GET.get(x, None) for x in date_kw('end'))):
            self.filter_errors['end_date'] = 'Incomplete date'

        if start_date:
            query = query.filter(Gallery.gallery_date >= start_date)
        if end_date:
            query = query.filter(Gallery.gallery_date <= end_date)

        return query

    @view_config(route_name='gallery_index', renderer='galleries/index.mako')
    def index(self):
        user = self.request.user
        years = range(2010, date.today().year + 1) + ['']
        months = range(1, 13) + ['']
        days = range(1, 32) + ['']

        search_components = dict(years = zip(years, years),
                months = zip(months, months), 
                days = zip(days, days),
                )
        
        if Role.GALLERY_ADMIN in user.role_ids:
            query = DBSession.query(Gallery) \
                    .join(Gallery.creator_detail)
        else:
            authorized_galleries = DBSession.query(Gallery.id) \
                    .join(Gallery.permission) \
                    .filter(GalleryPermission.role_id.in_(user.role_ids)) \
                    .group_by(Gallery.id)
            query = DBSession.query(Gallery) \
                    .join(Gallery.creator_detail) \
                    .filter(Gallery.id.in_(authorized_galleries))
        galleries = self.__paginate__(query, order='gallery_date', sort='desc')

        return {'galleries' : galleries,
                'search_components' : search_components,
                'filter_errors' : self.filter_errors,
                'request' : self.request}

    @view_config(route_name='gallery_new', renderer='galleries/new.mako', permission='gallery_admin')
    def new(self):
        user = self.request.user
        form = Form(self.request,
                schema=GallerySchema)
        if form.validate():
            #Generate a name for the new directory. Check if it exists.
            new_directory_name = None
            while not new_directory_name or (DBSession.query(Gallery).filter(Gallery.directory_name == new_directory_name).first()):
                new_directory_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(12))
                gallery_directory = self.request.registry.settings['gallery.directory']
                mkdir(path.join(gallery_directory, new_directory_name))
                mkdir(path.join(gallery_directory, new_directory_name, 'raw'))
                mkdir(path.join(gallery_directory, new_directory_name, 'thumbs'))
                mkdir(path.join(gallery_directory, new_directory_name, 'web'))
                data = form.data.copy()
                data['directory_name'] = new_directory_name
                data['created'] = datetime.now()
                data['creator'] = user.id
                #temporary
                del data['permissions']
            gallery = Gallery(**data)
            DBSession.add(gallery)
            DBSession.flush()
            return HTTPFound(self.request.route_url('gallery_view', id=gallery.id))

        return {'request' : self.request,
                'form_rend' : FormRenderer(form)}

    @view_config(route_name='gallery_view', renderer='galleries/view.mako')
    def view(self):

        gallery = Gallery.get(self.request.matchdict['id'], self.request.user)
        if gallery:
            media_query = DBSession.query(Medium).filter(
                    Medium.gallery_id == gallery.id)
            media = self.__paginate__(
                    media_query, order='medium_created', sort='desc')
            return {'request' : self.request,
                    'gallery' : gallery,
                    'media' : media}

        else:
            self.request.session.flash('Gallery not found')
            return HTTPFound(location=self.request.route_url('home'))

    @view_config(route_name='gallery_edit', renderer='galleries/edit.mako', permission='gallery_admin')
    def edit(self):
        user = self.request.user
        form = Form(self.request,
                schema=GallerySchema)
        gallery = DBSession.query(Gallery).get(self.request.matchdict['id'])
        roles = DBSession.query(Role).all()
        if form.validate():
            gallery.modified = datetime.now()
            gallery.last_update_by = user.id
            gallery.title = form.data['title']
            gallery.description = form.data['description']
            gallery.gallery_date = form.data['gallery_date']
            #Need to make an object exists validator
            temp_perms = []
            for existing_gallery_permission in gallery.permission:
                DBSession.delete(existing_gallery_permission)
            for r_id in form.data['permissions']:
                temp_perms.append(GalleryPermission(gallery_id = gallery.id,
                    role_id = r_id))
            gallery.permission[:] = temp_perms
                
            return HTTPFound(self.request.route_url('gallery_view', id=gallery.id))

        return {'request' : self.request,
                'gallery' : gallery,
                'roles' : roles,
                'form_rend' : FormRenderer(form)}

    @view_config(route_name='gallery_delete', renderer='json', permission='gallery_admin', request_method='POST')
    def delete(self):
        gallery_id = self.request.POST['id']
        gallery = DBSession.query(Gallery).get(gallery_id)

        #Check if the gallery is empty
        if len(gallery.media):
            self.request.session.flash('Gallery %s is not empty. Only empty galleries can be deleted' % gallery.title)
            return HTTPFound(location=self.request.route_url('gallery_index'))

        #Get the paths
        directory_path = path.join(self.request.registry.settings['gallery.directory'], gallery.directory_name)
        paths = [path.join(directory_path,'thumbs'),
                path.join(directory_path,'web'),
                path.join(directory_path,'raw'),
                path.join(directory_path)]

        #Delete the paths
        for dir_path in paths:
            rmdir(dir_path)

        #Delete the database record
        DBSession.delete(gallery)
        self.request.session.flash('Gallery %s was deleted' % gallery.title)
        return HTTPFound(location=self.request.route_url('gallery_index'))



        # - Add function to rebuild symlinks
    @view_config(route_name='gallery_rebuild_symlinks', renderer='json', permission='gallery_admin', request_method='POST')
    def rebuild_symlinks(self):
        '''In certain situations where the symlinks are not correct, this 
            action can be used to rebuild them'''
        #--------------
        # ToDO
        # - Exception handling in general
        #--------------

        gallery_id = self.request.POST['id']
        gallery = DBSession.query(Gallery).get(gallery_id)

        #Remove the directory
        directory_path = path.join(self.request.registry.settings['gallery.directory'], gallery.directory_name)
        shutil.rmtree(directory_path, True)

        #Recreate the directory tree for the gallery
        gallery_directory = self.request.registry.settings['gallery.directory']
        mkdir(path.join(gallery_directory, gallery.directory_name))
        mkdir(path.join(gallery_directory, gallery.directory_name, 'raw'))
        mkdir(path.join(gallery_directory, gallery.directory_name, 'thumbs'))
        mkdir(path.join(gallery_directory, gallery.directory_name, 'web'))

        #Loop through the images in the gallery and recreate the symlinks
        for media in gallery.media:
            for sub_directory in ['raw', 'web', 'thumbs']:
                sym_path = path.join(
                        self.request.registry.settings['gallery.directory'], 
                        gallery.directory_name, sub_directory, media.file_name)
                media_path = path.join(
                        self.request.registry.settings['gallery.directory'],
                        sub_directory, media.file_name)
                os.symlink(media_path,sym_path)

        return HTTPFound(location=self.request.route_url('gallery_index'))

