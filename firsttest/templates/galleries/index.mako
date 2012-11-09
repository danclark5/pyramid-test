<% from firsttest.models import Role%>
<%inherit file="/base.mako"/>
<%namespace name="pagination" file="/lib/paginate.mako"/>
<%block name="header">
  <script type="text/javascript" src="${request.static_url('firsttest:static/js/gallery/index.js')}"></script>
</%block>

${h.form(request.current_route_path(), 'get')}
  <fieldset>
  <legend> Search Galleries</legend>
    <div class="span-8 colborder">
      ${h.title('Title', label_for='title')} <br/>
      ${h.text('title', request.GET.get('title', ''), class_ = 'span-7')}
    </div>
    <div class="span-5 colborder">
      ${h.title('Start Date', label_for='title')} <br/>
      %if filter_errors.get('start_date',None):
      <span class="form_error"> ${filter_errors.get('start_date','')} </span><br/>
      %endif
      ${h.select('start_date_year', request.GET.get('start_date_year', ''), search_components['years'] )}
      ${h.select('start_date_month', request.GET.get('start_date_month', ''), search_components['months'] )}
      ${h.select('start_date_day', request.GET.get('start_date_day', ''), search_components['days'])} <br/>
      ${h.title(' End Date', label_for='title')} <br/>
      %if filter_errors.get('end_date',None):
      <span class="form_error"> ${filter_errors.get('end_date', '')} </span><br/>
      %endif
      ${h.select('end_date_year', request.GET.get('end_date_year', ''), search_components['years'])}
      ${h.select('end_date_month', request.GET.get('end_date_month', ''), search_components['months'])} 
      ${h.select('end_date_day', request.GET.get('end_date_day', ''), search_components['days'])} 
    </div>
    <div class="span-3 last">
      ${h.submit('', 'Search')}
    </div>
  </fieldset>
${h.end_form()}

<table class="span-24 last">
  <tr>
    <th> ${h.sort_by('Gallery Date', request=request)} </th>
    <th> ${h.sort_by('Title', request=request)} </th>
    <th> ${h.sort_by('Creator', request=request)} </th>
    <th class='center_text'> View</th>
    %if request.user and request.user.check_role(Role.GALLERY_ADMIN):
    <th class='center_text'> Update</th>
    <th class='center_text'> Delete</th>
    <th class='center_text'> Rebuild Symlinks</th>
    %endif
  </tr>
  %for i, gallery in enumerate(galleries):
   <tr class="${'odd' if i%2 else 'even'}">
    <td> ${gallery.gallery_date.strftime('%Y-%m-%d') if gallery.gallery_date else None} </td>
    <td> ${gallery.title} </td>
    <td> ${gallery.creator_detail.user} </td>
    <td class='center_text'> 
      <a href="${request.route_url('gallery_view', id = gallery.id)}">
        ${h.icon('page_go')}
      </a>
    </td>
    %if request.user and request.user.check_role(Role.GALLERY_ADMIN):
    <td class='center_text'> 
      <a href="${request.route_url('gallery_edit', id = gallery.id)}">
        ${h.icon('page_go')}
      </a>
    </td>
    <td>
      <form action="${request.route_url('gallery_delete')}" class="center_text delete_gallery" method="POST">
        ${h.hidden('id', gallery.id)}
        <input type="image" src="/static/img/icons/page_delete.png" alt="delete" class="center_text title_button">
      </form>
    </td>
    <td>
      <form action="${request.route_url('gallery_rebuild_symlinks')}" class="center_text refresh_gallery" method="POST">
        ${h.hidden('id', gallery.id)}
        <input type="image" src="/static/img/icons/page_refresh.png" alt="refresh" class="center_text title_button">
      </form>
    </td>
    %endif
  </tr>
  %endfor
</table>
<%pagination:pager paginator="${galleries}"/> 
