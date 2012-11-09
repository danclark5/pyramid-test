<%inherit file="/base.mako"/>
<%namespace name="form" file="/lib/form.mako"/>

${form_rend.begin(request.route_url('entry_new'))}

<div class="span-10">
${form_rend.label('title')}
<br/>
${form_rend.errorlist('title', class_='form_error')}
${form_rend.text('title', class_='span-10')}
</div>

<div class="span-5 last">
${form_rend.label('type')}
<br/>
${form_rend.errorlist('entry_type', class_='form_error')}
${form_rend.select('entry_type', (entry_types))}
</div>

<div class="span-23 last" >
${form_rend.label('entry')}
<br/>
${form_rend.errorlist('entry', class_='form_error')}
${form_rend.textarea('entry', class_='ckeditor')}
</div>

<%form:okcancel positive='Submit' negative='Cancel' />
${form_rend.end()}

