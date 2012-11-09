<%inherit file="/base.mako"/>
<%namespace name="form" file="/lib/form.mako"/>

<h2>
Add Gallery
</h2>

${form_rend.begin(request.route_url('gallery_new'))}

<div class="span-12">
${form_rend.label('title')}
<br/>
${form_rend.errorlist('title', class_='form_error')}
${form_rend.text('title', class_='span-10')}
</div>

<div class="span-12 last">
${form_rend.label('gallery date')}
<br/>
${form_rend.errorlist('gallery_date', class_='form_error')}
${form_rend.text('gallery_date', class_='span-10')}
</div>

<div class="span-24 last">
${form_rend.label('description')}
<br/>
${form_rend.errorlist('description', class_='form_error')}
${form_rend.textarea('description', class_='ckeditor')}
</div>

<%form:okcancel positive='Submit' negative='Cancel' />
${form_rend.end()}

