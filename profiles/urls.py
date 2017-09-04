from django.conf.urls import url

from .views import (
    WorkExperienceCreateView,
    EducationCreateView,
    user_quest_list_view,
    user_dashboard,
    profile_list_view,
    get_selected_user_profile,
)

urlpatterns = [
    url(r'^$', user_dashboard, name='user_dashboard'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/$', get_selected_user_profile, name='selected_user_profile'),
    url(r'^my_profile/$', profile_list_view, name='my_profile'),
    url(r'^my_profile/add_experience/$',
        WorkExperienceCreateView.as_view(),
        name='work_experience'),
    url(r'^quest_list/$', user_quest_list_view, name='user_quest_list'),
    url(r'^education/$', EducationCreateView.as_view(), name='education'),
]