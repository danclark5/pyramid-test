<%inherit file="/base.mako"/>
<%namespace name="form" file="/lib/form.mako"/>

<h2>
Edit Gallery
</h2>

${form_rend.begin(request.route_url('gallery_edit', id=gallery.id))}

<div class="span-12">
${form_rend.label('title')}
<br/>
${form_rend.errorlist('title', class_='form_error')}
${form_rend.text('title', class_='span-10', value=gallery.title)}
</div>

<div class="span-6">
${form_rend.label('gallery date')}
<br/>
${form_rend.errorlist('gallery_date', class_='form_error')}
${form_rend.text('gallery_date', class_='span-5', 
        value=gallery.gallery_date.strftime("%m/%d/%y") if gallery.gallery_date else None)}
</div>

<div class="span-6 last">
${form_rend.label('Permissions')}
<br/>
${form_rend.errorlist('permissions', class_='form_error')}
${form_rend.select('permissions', 
        options = ((role.id, role.name) for role in roles), 
        selected_value = (p.role_id for p in gallery.permission),
        multiple='multiple')}
</div>

<div class="span-24 last">
${form_rend.label('description')}
<br/>
${form_rend.errorlist('description', class_='form_error')}
${form_rend.textarea('description', class_='ckeditor', content=gallery.description)}
</div>


<%form:okcancel positive='Submit' negative='Cancel' />
${form_rend.end()}

