<%inherit file="base.mako"/>

%for entry in entries:
    <div class="entry">
        <h4 class="entry-title">
            ${entry.date} - ${entry.title}
        </h4>
        <% context.write(entry.entry) %>
    </div>
<br/>
<br/>
%endfor

