from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^registration/$',views.registration),
    url(r'^verifyDetails/$',views.verifyDetails),
    url(r'^deleteAll/$',views.deleteAll),
]