from formencode import Schema, validators
from formencode.foreach import ForEach

class EntrySchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

    title = validators.String(not_empty=True)
    entry = validators.String(not_empty=True)
    entry_type = validators.String(not_empty=True)

class GallerySchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

    title = validators.String(not_empty=True)
    gallery_date = validators.DateConverter(not_empty=True)
    description = validators.String(not_empty=True)
    permissions = ForEach(validators.Int()) 

class MediaNewSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

    id = validators.Int(not_empty=True)
    title = validators.String(not_empty=True)
    description = validators.String(not_empty=True)
