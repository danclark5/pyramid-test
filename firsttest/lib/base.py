import webhelpers.paginate as paginate 

from sqlalchemy import asc, desc

class BaseView(object):

    orderings = {}

    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __filter__(self, query):
        return query

    def __paginate__(self, query, page=1, count=20, order=None, sort='asc'):
        url = paginate.PageURL_WebOb(self.request)

        ordering  = self.request.GET.get('order', order)
        sort_func = desc if self.request.GET.get('sort', sort) == 'desc' else asc

        if ordering in self.orderings:
            query = query.order_by(sort_func(self.orderings[ordering]))

        query = self.__filter__(query)

        return paginate.Page(query, 
                url = url,
                page = int(self.request.GET.get('page', page)),
                items_per_page=int(self.request.GET.get('count', count)))
            
