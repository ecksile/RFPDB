from django.conf.urls import patterns, include, url
from RFPDB.views import hello, add, ans_search, loaddoc, upload_file

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                      (r'^hello/$', hello),
                      (r'^add/$', add),
                      (r'^search/$', ans_search),
                      (r'^loaddoc/$', loaddoc),
                      (r'^upload/$', upload_file),
    # Examples:
    # url(r'^$', 'RFPDB.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       
    url(r'^admin/', include(admin.site.urls)),
)
