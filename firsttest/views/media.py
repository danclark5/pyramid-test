from pyramid.view import view_config
from pyramid.response import Response, FileResponse
from pyramid.httpexceptions import HTTPFound
from pyramid_simpleform import Form

from firsttest.lib.base import BaseView
from firsttest.lib.forms import MediaNewSchema
from firsttest.models import DBSession, Medium, Gallery, MediumType
from os import path, mkdir, remove
import os, uuid
import sys
from datetime import datetime
from PIL import Image 
import shutil, fcntl

class UploadError(Exception):
    def __init__(self, value):
        self.value = value
        print 'Error : ' + value
    def __str__(self):
        return repr(self.value)

class MediaViews(BaseView):

    allowed_extensions = ['.JPG']

    def __sanitize_file_name(self, file_name):
        '''Clean up the name of the file being uploaded.'''
        print '#' * 80
        #Get the name and the extension
        self.upload_full_name = path.split(file_name)[1]
        #Everything before the dot for the extension
        self.upload_name = path.splitext(self.upload_full_name)[0]
        #Everything after the dot for the extension
        self.upload_extension = path.splitext(self.upload_full_name)[1].upper()
        self.upload_full_name = self.upload_name + self.upload_extension
        print self.upload_full_name
        print self.upload_name
        print self.upload_extension

        #Check that the file type is legal 
        if self.upload_extension not in self.allowed_extensions:
            #Change to raised exception
            raise UploadError('Invalid File Type')
        

    def __check_file_existance(self):
        '''Check if a file possibly exists in the file system. If it does then
            append a short unique identifier to make the name unique.'''
        #First check the Media table to see if it present. We will onlygg allow
        # the name to occur once.
        medium = (DBSession.query(Medium)
                .filter(Medium.file_name == self.upload_full_name)
                .first())
        if medium:
            uid = '__' + str(uuid.uuid4())[0:8]
            self.upload_full_name = self.upload_name + uid + self.upload_extension

    def __save_jpeg(self, media, gallery, sub_directory, max_size=None, create_symlink=True):
        '''Save the media being uploaded that path is the one desginated by 
            self.gallery_path.
        -file: The file be saved
        -gallery: The gallery that the file will be saved under.
        -max_size: the maximum size that either the width or height should 
            be. If this is not designated then the image is saved unaltered
        -sub_directory: Saves the image to a subdirectory within the target
            directory'''
        print '$' * 80
        print 'saving image'

        #--------------
        # ToDO
        # - Better exception handling
        #--------------
        
        #path of actual file in the root/subdirectory
        media_path = path.join(
                self.request.registry.settings['gallery.directory'],
                sub_directory, self.upload_full_name)
        media.seek(0)
        try:
            readied_media = Image.open(media)
            if max_size:
                size = max_size, max_size
                readied_media.thumbnail(size)
            fd = os.open(media_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, 'w') as target_media:
                readied_media.save(target_media, 'JPEG')
        except IOError as e:
            print 'cannot save media:', self.upload_full_name, ': ', e
            raise UploadError('IOError : Unable to save picture')
        except:
            raise UploadError('Unable to save picture due')
        #need to add other exceptions for other errors.

        #Save the symlink
        if create_symlink:
            try:
                sym_path = path.join(
                        self.request.registry.settings['gallery.directory'], 
                        gallery.directory_name, sub_directory, 
                        self.upload_full_name)
                os.symlink(media_path,sym_path)
            except:
                raise UploadError('Unable to create symlinks')


    @view_config(route_name='media_upload', renderer='json', permission='gallery_admin')
    def upload(self):
        #--------------
        # ToDO
        # - Better exception handling
        # - Add cleanup when exception occurs
        #   - Remove any files that were uploaded, but be careful about errors
        #       that occur because the file already exists.
        #   - Remove media record if it exists.
        # - Add support for PNG?
        # - Videos?
        #--------------
        #check the directory in the request against the Gallery directory
        user = self.request.user
        gallery = DBSession.query(Gallery).get(self.request.POST['id'])
        if not gallery or gallery.directory_name != self.request.POST['dir']:
            return Response(status_int=409)

        try:
            self.__sanitize_file_name(self.request.POST['Filename'])
            self.__check_file_existance()
            #sys.exit()

            input_file = self.request.POST['Filedata'].file
            self.__save_jpeg(input_file, gallery, 'original', create_symlink = False)
            self.__save_jpeg(input_file, gallery, 'raw')
            self.__save_jpeg(input_file, gallery, 'thumbs', 150)
            self.__save_jpeg(input_file, gallery, 'web', 800)
        except UploadError:
            return Response(status_int=409)
        except:
            return Response(status_int=409)

        #add database record
        medium = Medium(file_name = self.upload_full_name, 
                      created = datetime.now(),
                      creator = user.id,
                      gallery_id = gallery.id,
                      media_type = MediumType.IMAGE)
        DBSession.add(medium)
            
        return Response('ok', status_int=200) 

    @view_config(route_name='media_update_ajax', renderer='json', permission='gallery_admin', xhr=True, request_method='POST')
    def update_ajax(self):

        form = Form(self.request,
                schema=MediaNewSchema)
        if form.validate():

            medium = DBSession.query(Medium).get(form.data['id'])
            medium.title = form.data['title']
            medium.description = form.data['description']
            return Response('ok', status_int=200) 
        else:
            return Response('error', status_int=400) 

    @view_config(route_name='media_delete', renderer='json', permission='gallery_admin', xhr=True, request_method='POST')
    def delete(self):
        medium_id = self.request.POST['id']
        medium = DBSession.query(Medium).get(medium_id)
        #build the paths to delete
        phy_path = self.request.registry.settings['gallery.directory']
        sym_path = path.join(self.request.registry.settings['gallery.directory'], medium.gallery.directory_name)
        paths = [path.join(phy_path,'raw',medium.file_name),
                path.join(phy_path,'original',medium.file_name),
                path.join(phy_path,'thumbs',medium.file_name),
                path.join(phy_path,'web',medium.file_name),
                path.join(sym_path,'raw',medium.file_name),
                path.join(sym_path,'thumbs',medium.file_name),
                path.join(sym_path,'web',medium.file_name)]
        for file_path in paths:
            remove(file_path)
        DBSession.delete(medium)
        return Response('ok')

    @view_config(route_name='media_view')
    def view(self):
        user = self.request.user
        medium_id = self.request.matchdict['medium_id']
        media_type = self.request.matchdict['type']
        medium = Medium.get(medium_id, user)
        if medium:
            subdirectory = media_type if media_type in ['thumbs', 'web', 'raw'] else None
            if subdirectory:
                media_path = path.join(self.request.registry.settings['gallery.directory'], 
                        medium.gallery.directory_name, subdirectory, medium.file_name)
            else:
                media_path = path.join(self.request.registry.settings['gallery.directory'], 
                        medium.gallery.directory_name, medium.file_name)
            return FileResponse(media_path)
        else:
            self.request.session.flash('Media not found')
            return HTTPFound(location=self.request.route_url('home'))

    @view_config(route_name='media_rotate', renderer='json', permission='gallery_admin')
    def rotate(self):
        #TODO: Need to get a media type flag in the media table
        medium_id = self.request.matchdict['medium_id'] 
        direction = int(self.request.POST.get('direction'))
        if direction % 90 != 0:
            raise ValueError
        medium = DBSession.query(Medium).get(medium_id)
        lock_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'gallery.lock')
        medium_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'raw', medium.file_name)
        web_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'web', medium.file_name)
        thumb_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'thumbs', medium.file_name)
        try:
            with open(lock_path, 'a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with open(medium_path, 'r') as original_raw:
                   #create lock 
                   fcntl.flock(original_raw, fcntl.LOCK_EX | fcntl.LOCK_NB)
                   original_media = Image.open(original_raw)
                   rotated_media = original_media.rotate(direction)
                   thumb_media = rotated_media.copy()
                   web_media = rotated_media.copy()
                   rotated_media.save(medium_path)
                   #save the thumb version
                   thumb_media.thumbnail((150, 150))
                   thumb_media.save(thumb_path)
                   #save the web version
                   web_media.thumbnail((800, 800))
                   web_media.save(web_path)
                   #release the lock
                   fcntl.flock(original_raw, fcntl.LOCK_UN)
                fcntl.flock(lock, fcntl.LOCK_UN)
        except:
            raise
            return Response('error')
        else:
            return Response('ok')

    @view_config(route_name='media_restore', renderer='json', permission='gallery_admin')
    def restore(self):
        medium_id = self.request.matchdict['medium_id'] 
        medium = DBSession.query(Medium).get(medium_id)
        original_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'original', medium.file_name)
        raw_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'raw', medium.file_name)
        web_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'web', medium.file_name)
        thumb_path = path.join(
                self.request.registry.settings['gallery.directory'],
                'thumbs', medium.file_name)
        try:
            with open(original_path, 'r') as original_raw:
               original_media = Image.open(original_raw)
               #restore thumb version
               thumb_media = original_media.copy()
               thumb_media.thumbnail((150, 150))
               thumb_media.save(thumb_path)
               #restore web version
               web_media = original_media.copy()
               web_media.thumbnail((800, 800))
               web_media.save(web_path)
               #restore raw
               original_media.save(raw_path)
        except:
            raise
            return Response('error')
        else:
            return Response('ok')
