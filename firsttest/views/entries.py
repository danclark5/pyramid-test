from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from datetime import datetime, date

from firsttest.lib.base import BaseView
from firsttest.lib.forms import EntrySchema 
from firsttest.models import DBSession, Entry, EntryType

class EntryViews(BaseView):

    orderings = {'date' : Entry.date,
            'title' : Entry.title,
            'entry_type' : EntryType.description}

    def __filter__(self, query):
        self.filter_errors = {}
        title = self.request.GET.get('title', None)
        entry_type = self.request.GET.get('entry_type', None)

        if title:
            title = '%' + title.replace(' ', '%') + '%'
            query = query.filter(Entry.title.like(title))
    

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
            query = query.filter(Entry.date >= start_date)
        if end_date:
            query = query.filter(Entry.date <= end_date)
        if entry_type:
            query = query.filter(Entry.entry_type == entry_type)

        return query

    @view_config(route_name='entry_index', renderer='entries/index.mako', permission='owner')
    def index(self):
        #Generate the supporting data for the search form
        years = range(2010, date.today().year + 1) + ['']
        months = range(1, 13) + ['']
        days = range(1, 32) + ['']
        entry_types = [(i.id, i.description) for i in DBSession.query(EntryType).all()] + [('', '')]
        search_components = dict(years = zip(years, years),
                months = zip(months, months), 
                days = zip(days, days),
                entry_types = entry_types
                )
        query = DBSession.query(Entry) \
            .join(EntryType)
        entries = self.__paginate__(query, order='date', sort='desc')
        return {'entries' : entries,
                'search_components' : search_components,
                'filter_errors' : self.filter_errors,
                'request' : self.request}

    @view_config(route_name='entry_view', renderer='entries/view.mako', permission='owner')
    def view(self):
        query = DBSession.query(Entry) \
            .filter(Entry.id == self.request.matchdict['id'])
        entry = query.first()
        return {'entry' : entry,
                'request' : self.request}

    @view_config(route_name='entry_edit', renderer='entries/edit.mako', permission='owner')
    def edit(self):
        entry_id = self.request.matchdict['id']
        entry = DBSession.query(Entry).get(entry_id)
        entry_types = list((i.id, i.description) for i in DBSession.query(EntryType).all())
        entry_types.append(('', ''))

        form = Form(self.request,
                schema=EntrySchema,
                obj=entry)

        if form.validate():
            #TODO: This would be nice
            #entry.update(**form.data)
            entry.title = form.data['title']
            entry.entry_type= form.data['entry_type']
            entry.entry = form.data['entry']

            return HTTPFound(location="/")

        return {'request' : self.request,
                'entry' : entry, 
                'entry_types' : entry_types,
                'form_rend' : FormRenderer(form)}

    @view_config(route_name='entry_new', renderer='entries/new.mako', permission='owner')
    def new(self):

        entry_types = list((i.id, i.description) for i in DBSession.query(EntryType).all())
        entry_types.append(('', ''))

        form = Form(self.request,
                schema=EntrySchema)

        if form.validate():
            data = form.data.copy()
            data['date'] = datetime.now()
            DBSession.add(Entry(**data))
            return HTTPFound(location="/")

        return {'request' : self.request,
                'entry_types' : entry_types,
                'form_rend' : FormRenderer(form)}

    @view_config(route_name='entry_delete', request_method='POST', permission='owner')
    def delete(self):
        entry_id = self.request.POST['id']
        entry = DBSession.query(Entry).get(entry_id)
        self.request.session.flash('Deleted "%s" entry' % entry.title)
        DBSession.delete(entry)
        return HTTPFound(location=self.request.route_url('entry_index'))
