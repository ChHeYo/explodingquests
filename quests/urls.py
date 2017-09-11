from django.conf.urls import url

from .views import (
    QuestListView, QuestDetailView,
    CreateQuest, DeleteQuestView,
    UpdateQuestView,
    get_selected_user_list,
    edit_quest_images,
    delete_quest_images,
    interested_users_list,
    get_selected_user_profile,
    MessageCreateView,
    DiffuseToggle,
)

urlpatterns = [
    # url(r'^$', QuestListView.as_view(), name='homepage'),
    url(r'^create/$', CreateQuest.as_view(), name='create_quest'),
    url(r'^(?P<slug>[\w-]+)/$', QuestDetailView.as_view(), name='quest_detail'),
    url(r'^(?P<slug>[\w-]+)/images/$', edit_quest_images, name='edit_quest_images'),
    url(r'^delete/(?P<id>[\w-]+)/$', delete_quest_images, name='delete_quest_images'),
    url(r'^(?P<slug>[\w-]+)/defuse/$', DiffuseToggle.as_view(), name='diffuse'),
    url(r'^(?P<slug>[\w-]+)/interested/$', interested_users_list, name='interested_users'),
    url(r'^(?P<slug>[\w-]+)/interested/(?P<username>[a-zA-Z0-9]+)/$',
        get_selected_user_profile, name='selected_user_profile'),
    url(r'^(?P<slug>[\w-]+)/interested/(?P<username>[a-zA-Z0-9]+)/send_msg/$',
        MessageCreateView.as_view(), name='send_message'),
    url(r'^(?P<slug>[\w-]+)/update/$', UpdateQuestView.as_view(), name='update_quest'),
    url(r'^(?P<slug>[\w-]+)/delete/$', DeleteQuestView.as_view(), name='delete_quest'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/quest_list/$', get_selected_user_list, name='selected_user_list'),
]