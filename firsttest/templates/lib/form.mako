<%def name="okcancel(positive, negative, negative_url=None, *args, **kwargs)">
<% negative_url = negative_url or request.environ.get('HTTP_REFERER', None) or '/' %>
<div class="submit right">
  <a class="valign button negative" href="${negative_url}">
    ${h.image(kwargs.get('negative_icon', '/static/img/icons/cross.png'), negative)}
    <span>${negative}</span>
  </a>
  <button type="submit" class="positive">
    ${h.image(kwargs.get('positive_icon', '/static/img/icons/tick.png'), positive)}
    <span>${positive}</span>
  </button>  
</div>
</%def>
