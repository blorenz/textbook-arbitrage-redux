from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TextbookArb.views.home', name='home'),
    # url(r'^TextbookArb/', include('TextbookArb.foo.urls')),
    url(r'^deals/$', 'ta.views.getDeals'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^launch/$', 'ta.views.launch'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'ta.views.loginThing'),
    url(r'^logout/$', 'ta.views.logout_user'),
    url(r'^lazy/$', 'ta.views.lazy'),
    url(r'^cats/$', 'ta.views.defineCategories'),
    url(r'^historical/$', 'ta.views.getHistoricalPrices'),
    url(r'^known/$', 'ta.views.known'),
)




urlpatterns += staticfiles_urlpatterns()
