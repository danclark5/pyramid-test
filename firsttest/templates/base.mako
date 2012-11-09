<!DOCTYPE HTML>
<% from firsttest.models import Role, User%>
<html>
  <head>
    <title> Dan Clark - Developer</title>
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/blueprint/screen.css')}" type="text/css" media="screen, projection"/>
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/blueprint/plugins/buttons/screen.css')}" type="text/css" media="screen, projection"/>
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/blueprint/print.css')}" type="text/css" media="print"/>
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/stickyfooter.css')}" type="text/css" media="screen"/>
    <!--[if lt IE 8]>
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/blueprint/ie.css')}" type="text/css" media="screen, projection"/>
    <![endif]-->
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/layout.css')}" type="text/css" media="screen"/>
    <link rel="stylesheet" href="${request.static_url('firsttest:static/css/general.css')}" type="text/css" media="screen"/>
    <script src="${request.static_url('firsttest:static/js/jquery-1.7.2.min.js')}"></script>
    <script src="${request.static_url('firsttest:static/js/jquery.tools.min.js')}"></script>
    <script src="${request.static_url('firsttest:static/js/base.js')}"></script>
    <script type="text/javascript" src="${request.static_url('firsttest:static/ckeditor/ckeditor.js')}"></script>
    <%block name="header"/> 
  </head>
  <body>
    <div class = "fence">
    </div>
    <div class="centerPopup">
        <img src="/static/img/ajax-loader.gif"/>
    </div>
    <div id="wrap">
    <div class="white-background">
    <header class="container">
	    <h1 id="banner">
          <a href="#">Dan Clark</a>
		</h1>
    </header>
    </div>
    <div class="green-background">
	  <nav class="clearfix container">
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          ##<li><a href="#">Resume</a></li>
          ##<li><a href="#">Contact</a></li>
          %if request.user and request.user.check_role(Role.OWNER):
          <li><a href="/entry/index">Entries</a><ul>
            <li><a href="/entry/new">New Entry</a></li></ul>
          %endif
          <li><a href="/gallery/index">Galleries</a>
          %if request.user and request.user.check_role(Role.GALLERY_ADMIN):
            <ul><li><a href="/gallery/new">New Gallery</a></li></ul>
          %endif
          </li>
          %if request.user.user != User.VISITOR: 
          <li><a href="/logout">Log Out</a></li>
          %else: 
          <li><a href="/login">Login</a></li>
          %endif
	  </nav>
    </div>
      <div id="main" class="container">
        ${self.flash_messages()}
        ${self.body()}
	  </div>
    </div>
    <div id="footer" class="green-background">
	  <footer class="container">
	    "Amazing-looking ship though. Looks like a fish, moves like a fish, steers like a cow."
      </footer>
	</div>
  </body>
</html>

<%def name="flash_messages()">
  %if request.session.peek_flash():
    <% flash = request.session.pop_flash() %>
    %for message in flash:
    <div class="alert-message">
        <a class="close" href="#">X</a>
        <div>
            <p> ${message} </p>
        </div>
    </div>
    %endfor
  %endif
</%def>
