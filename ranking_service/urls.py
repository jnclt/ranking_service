from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^rankings/', 'rankings.views.handle_ranking_request'),
                       )
