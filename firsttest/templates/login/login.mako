<%inherit file="/base.mako"/>
<form action="" method="post">
  <input type="hidden" name="came_from" value="${came_from}"/>
  ${h.title('Login', label_for='login')} <br/>
  ${h.text('login', (login or ''))} <br/>
  ${h.title('Password', label_for='password')} <br/>
  ${h.password('password', (password or ''))} <br/>
  <input type="submit" name="form.submitted" value="Log In"/>
</form>
