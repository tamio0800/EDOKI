from django.urls import path, re_path
from django.conf.urls import handler400, handler403, handler404, handler500
from . import views

urlpatterns = [
    path("edoki/", views.index, name="index"),
    path("", views.index, name="index_nohead"),
    path("edoki/wiki/<str:title>/", views.wiki_entry, name="wiki_entry"),
    re_path(r"edoki/wiki/(?P<title>).*[\s\w]*/$", views.wiki_entry, name="wiki_entry"),
    re_path(
        r"edoki/update-entry/$",
        views.create_update,
        name="create_update",
    ),
    re_path(
        r"edoki/update-entry/?/(?P<title>.*\s*)/$",
        views.create_update,
        name="create_update",
    ),
    re_path(
        r"edoki/delete-entry/(?P<title>)/?(?P<deletion>.*)/$",
        views.delete_entry,
        name="delete_entry",
    ),
    path("edoki/delete-entry/<title>/<deletion>", views.delete_entry, name="delete_entry"),
    path("edoki/delete-entry/<title>", views.delete_entry, name="delete_entry"),
    path("edoki/random-entry/", views.random_entry, name="random_entry"),
    re_path(r"edoki/page-not-found/$", views.notFound, name="notFound"),
]
