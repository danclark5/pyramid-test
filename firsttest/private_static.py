from pyramid.static import static_view
private_static_view = static_view('firsttest:priv_res', use_subpath=True)
