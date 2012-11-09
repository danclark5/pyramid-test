<% 
  import string 
  import itertools
  from firsttest.models import Role 
%>
<%inherit file="/base.mako"/>
<%namespace name="pagination" file="/lib/paginate.mako"/>
<%block name="header">
  <script type="text/javascript" src="${request.static_url('firsttest:static/js/gallery/view.js')}"></script>
  <script type="text/javascript" src="${request.static_url('firsttest:static/js/jquery.uploadify-3.1.min.js')}"></script>
  <link rel="stylesheet" type="text/css" href="${request.static_url('firsttest:static/css/uploadify.css')}" />
  <link rel="stylesheet" type="text/css" href="${request.static_url('firsttest:static/css/simple_overlay.css')}" />

</%block>

<h2>
${gallery.title} Gallery
</h2>
%if request.user and request.user.check_role(Role.GALLERY_ADMIN):
<input type="file" name="file_upload" id="file_upload" /> 
%endif
<div>
%if len(media) == 0:
This gallery contains no items
%else:
  <%
    prior = [None] + media[:-1] 
    peak = media[1:] + [None]
    media_list = zip(prior, media, peak)%>
  %for medium in media_list:
  <div class="media_container">
  <div class="left media_thumb">
    <img src="${request.route_url('media_view', medium_id= medium[1].id, type = 'thumbs')}" 
         alt="${medium[1].title if medium[1].title else medium[1].file_name}"
         rel="${'#img_'+str(medium[1].id)}"
         title="test"/>
  </div>
  <div class="simple_overlay" id="${'img_'+str(medium[1].id)}">
    <div class="close">X</div>
    <div class="caption">
      %if medium[0] is not None:
      ${h.icon('resultset_previous', rel=('#img_' + str(medium[0].id)))}
      %endif
      %if medium[2] is not None:
      ${h.icon('resultset_next', rel=('#img_' + str(medium[2].id)))}
      %endif
      <span class="medium_title">${medium[1].title if medium[1].title else medium[1].file_name}</span>
      <a href="${request.route_url('media_view', medium_id= medium[1].id, type = 'raw')}"> Full Size </a>
%if request.user and request.user.check_role(Role.GALLERY_ADMIN):
      <span class="edit_medium faux_link">Edit</span>
      <span class="delete_medium faux_link" id="${medium[1].id}">Delete</span>
      <span class="restore_medium faux_link" id="${medium[1].id}">Restore</span>
      <span class="rotate_l_medium faux_link" id="${medium[1].id}">${h.icon('arrow_rotate_anticlockwise')}</span>
      <span class="rotate_r_medium faux_link" id="${medium[1].id}">${h.icon('arrow_rotate_clockwise')}</span>
%endif
    </div>
%if request.user and request.user.check_role(Role.GALLERY_ADMIN):
    <div class="edit_title">
      <input type="text" class="title_value input" value="${medium[1].title if medium[1].title else 'Please enter a title...'}"/>
      <span class="edit_medium_next">Next</span>
      <span class="cancel">Cancel</span>
    </div>
    <div class="edit_descr span-5">
      <textarea class="descr_value input">${medium[1].description if medium[1].description else 'Please enter a description...'}</textarea>
      <span class="cancel">Cancel</span>
      <span class="edit_medium_done" id="${medium[1].id}">Done</span>
    </div>
    <div class="edit_failed span-5">
      Edit failed
      <span class="cancel">OK</span>
    </div>
%endif
    <div> 
    <div class="medium_descr"> ${medium[1].description if medium[1].description else ''} </div>
    <img src="${request.route_url('media_view', medium_id = medium[1].id, type = 'web')}" class="medium"/> 
    </div>
  </div>
  </div>

  %endfor;
%endif
</div>
<script>
    var gallery = {'id' : '${gallery.id}', 'dir' : '${gallery.directory_name}'}
</script>
<%pagination:pager paginator="${media}"/> 
