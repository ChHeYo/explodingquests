"""explodingquests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from django.views.generic import TemplateView
from quests.views import (
    QuestListView,
    get_user_settings,
    password_change_page_view,
    account_inactive_redux,
    email_verification_redux,
)


urlpatterns = [
    url(r'^$', QuestListView.as_view(), name='homepage'),
    url(r'^quests/', include('quests.urls', namespace='quests')),
    url(r'^accounts/password/change/$', password_change_page_view, name='account_change_password'),
    url(r'^accounts/inactive/$', account_inactive_redux, name='account_inactive'),
    url(r'^accounts/confirm-email/$', email_verification_redux, name='account_email_verification_sent'),
    url(r'^accounts/settings/$', get_user_settings, name='user_settings'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^dashboards/', include('profiles.urls', namespace='dashboard')),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]