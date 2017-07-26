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
    HomePageTemplateView, CreateQuest,
    QuestListView, QuestDetailView,
    DeleteQuestView, UpdateQuestView,
    get_user_profile,
)

urlpatterns = [
    url(r'^$', QuestListView.as_view(), name='homepage'),
    url(r'^quest/(?P<slug>[\w-]+)/$', QuestDetailView.as_view(), name='quest_detail'),
    url(r'^update/(?P<slug>[\w-]+)/$', UpdateQuestView.as_view(), name='update_quest'),
    url(r'^delete/(?P<slug>[\w-]+)/$', DeleteQuestView.as_view(), name='delete_quest'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/create/$', CreateQuest.as_view(), name='create_quest'),
    url(r'^accounts/settings/$', get_user_profile, name='user_profile'),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]