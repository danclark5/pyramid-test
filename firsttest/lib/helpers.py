# your helpers imports  
from webhelpers.html.tags import *
from webhelpers.html.builder import make_tag

def update_params(request, **kwargs):
    '''Updates the parameters of a request with values passed in through kwargs'''
    params = request.GET.mixed()
    params.update(kwargs)
    return params

def icon(name, **kwargs):	
    '''Returns an image tag for the requested image'''
    return image('/static/img/icons/%s.png' % name, name, **kwargs)

def sort_by(label, request, order=None, **kwargs):
    '''Generates and returns a HTML tag that allows the user to sort a query result'''
    order = order if order else label.lower().replace(' ', '_')
    current = False
    if 'order' in request.GET and request.GET['order'] == order:        
        sort = 'desc' if request.GET.get('sort') == 'asc' else 'asc'
        current = True
    else:
        sort = 'asc'
    inner = make_tag('span', label, class_='valign')
    if current:
        inner = inner + icon('bullet_arrow_down' if sort == 'asc' else 'bullet_arrow_up', class_='valign')
        
    return make_tag('a', 
            inner, 
            href=request.current_route_url(_query=update_params(
                request=request, page=1, order=order, sort=sort)), 
            class_='noline', 
            **kwargs)

def edit_button(request, view_class):
    '''Generates an edit button link. Requires the view class as a parameter,
        but it would be nice to get this from the request'''
    return make_tag('a',
            image('/static/img/editSM.png', 'edit'),
            href=request.route_url('%s_edit' % view_class, id=request.matchdict['id']),
            class_='title_button',
            )

def delete_button(request, view_class):
    '''Generates an delete button link. Requires the view class as a parameter,
        but it would be nice to get this from the request'''
    return make_tag('a',
            image('/static/img/delSM.png', 'delete'),
            href=request.route_url('%s_delete' % view_class, id=request.matchdict['id']),
            class_='title_button',
            )
def url(request, **kwargs):
    '''Generates a link'''
    return request.current_route_url(_query = kwargs)



