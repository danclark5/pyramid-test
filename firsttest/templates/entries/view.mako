<%inherit file="/base.mako"/>
<%block name="header">
  <script type="text/javascript" src="${request.static_url('firsttest:static/js/entry/view.js')}"></script>
</%block>

<div class="entry">
  <h4 class="entry-title">
    ${entry.date} - ${entry.title} - ${entry.entry_type_detail.description}
    <form action="${request.route_url('entry_delete')}" class="center delete_gallery" id="delete_entry" method="POST">
        ${h.hidden('id', entry.id)}
        <input type="image" src="/static/img/delSM.png" alt="delete" class="title_button">
    </form>
    ${h.edit_button(request, 'entry')}
  </h4>
  <% context.write(entry.entry) %>
</div>
