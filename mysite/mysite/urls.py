"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from dm.views import *

from dm.views import addmovieomdb
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','dm.views.show_main',name="show_main"),
    url(r'^addmovieomdb$','dm.views.addmovieomdb',name="addmovieomdb"),
    url(r'^try1$','dm.views.try1',name="try1"),
    url(r'^try2$','dm.views.try2',name="try2"),
    url(r'^getname$','dm.views.getname',name="getname"),
    url(r'^gettweets$','dm.views.gettweets',name="gettweets"),
    url(r'^getrating$','dm.views.getrating',name="getrating"),
    
    url(r'^recommend$','dm.views.recommend',name="recommend")
    
]
