<%def name="pager(paginator)">
<div class="pager">
  <div>
    ${ paginator.pager('<strong>Results:</strong> $first_item to $last_item of $item_count') }
  </div>
  <div class="navigator">
    ${ paginator.pager('$link_first $link_previous ~2~ $link_next $link_last', 
                       symbol_first=h.icon('resultset_first'), 
                       symbol_last=h.icon('resultset_last'),
                       symbol_previous=h.icon('resultset_previous'), 
                       symbol_next=h.icon('resultset_next'))} 
  </div>
  %if paginator.item_count > 25:
  <div class="result_size">
    <strong>Results per Page:</strong> 
    ${h.link_to(25, h.url(request, count=25), class_="cur_size" if request.GET.get('count') == '25' else None)} 
    ${h.link_to(50, h.url(request, count=50), class_="cur_size" if request.GET.get('count') == '50' else None) } 
    ${h.link_to(100, h.url(request, count=100), class_="cur_size" if request.GET.get('count') == '100' else None) }
  </div>
  %endif
</div>	
</%def>

