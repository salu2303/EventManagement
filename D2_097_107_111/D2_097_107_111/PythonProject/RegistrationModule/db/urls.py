from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^ViewCustomers/$',views.ViewCustomers),
    url(r'^ViewManagers/$',views.ViewManagers),
    url(r'^ViewAdmin/$',views.ViewAdmin),
    url(r'^ViewCustomerEvents/$',views.ViewCustomerEvents),
    url(r'^ViewAdminEvents/$',views.ViewAdminEvents),
    url(r'^ViewManagerEvents/$',views.ViewManagerEvents),
    url(r'^ViewEvents/$',views.ViewEvents),
    url(r'^All/',views.All),
    url(r'^ViewImages/',views.ViewImages),
    url(r'^ViewVideos/',views.ViewVideos),
]