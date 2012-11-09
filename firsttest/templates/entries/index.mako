<%inherit file="/base.mako"/>
<%namespace name="pagination" file="/lib/paginate.mako"/>

${h.form(request.current_route_path(), 'get')}
  <fieldset>
  <legend> Search Entries </legend>
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
    <div class="span-5">
      ${h.title('Entry Type', label_for='entry_type')} <br/>
      ${h.select('entry_type', request.GET.get('entry_type', ''), search_components['entry_types'])}
    </div>
    <div class="span-3 last">
      ${h.submit('', 'Search')}
    </div>
  </fieldset>

${h.end_form()}

<table class="span-24 last">
  <tr>
    <th> ${h.sort_by('Date', request=request)} </th>
    <th> ${h.sort_by('Title', request=request)} </th>
    <th> ${h.sort_by('Entry Type', request=request)} </th>
    <th class='center_text'> View</th>
  </tr>
  %for i, entry in enumerate(entries):
  <tr class="${'odd' if i%2 else 'even'}">
    <td> ${entry.date.strftime('%Y-%m-%d %I:%M %p')} </td>
    <td> ${entry.title} </td>
    <td> ${entry.entry_type_detail.description} </td>
    <td class='center_text'> 
      <a href="${request.route_url('entry_view', id = entry.id)}">
        ${h.icon('page_go')}
      </a>
     </td>
  </tr>
  %endfor
</table>
<%pagination:pager paginator="${entries}"/> 
