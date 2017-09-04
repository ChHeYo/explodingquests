from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import CreateView, ListView
from django.utils import timezone

from quests.models import UserProfile, Quest

from .models import Education, WorkExperience
from .forms import EducationForm, WorkExperienceForm

# Create your views here.


@login_required
def profile_list_view(request):

    initial_list = [''] * 3
    experience, education, profile_img = initial_list
    
    try:
        experience = get_list_or_404(WorkExperience, user=request.user)
        education = get_list_or_404(Education, user=request.user)
        profile_img = get_object_or_404(UserProfile, user=request.user)
    except:
        # msg = 'No profile'
        # raise ObjectDoesNotExist(msg)
        pass

    context = {
        'experiences': experience,
        'educations': education,
        'profile_img': profile_img,
    }

    return render(request, 'profiles/profile_list.html', context)


@login_required
def user_quest_list_view(request):
    user_quest_list = ''
    try:
        user_quest_list = Quest.objects.filter(user=request.user, explosion_datetime__gte=timezone.now())
        user_quest_list_count = user_quest_list.count()
        all_quest = Quest.objects.all()
        defused_quests = all_quest.filter(interested_users=request.user)
        defused_quests_count = defused_quests.count()
        # active_list = user_quest_list.filter(explosion_datetime__lte=timezone.now())
        # exploded_list = user_quest_list.filter(explosion_datetime__gte=timezone.now())
    except ObjectDoesNotExist:
        msg = "No quest"
        raise ObjectDoesNotExist(msg)
    context = {
        'list': user_quest_list,
        'count': user_quest_list_count,
        'def_quests': defused_quests,
        'def_quest_count': defused_quests_count,
        # 'actives': active_list,
        # 'exploded': exploded_list,
    }
    return render(request, 'account/user_quest_list.html', context)


@login_required
def user_dashboard(request):
    profile_pic = get_object_or_404(UserProfile, user=request.user)
    template_name = 'account/user_dashboard.html'
    context = {
        'profile_pic': profile_pic,
    }
    return render(request, template_name, context)


@login_required
def get_selected_user_profile(request, username):
    
    initial_list = [''] * 4
    user, experience, education, profile_img = initial_list

    try:
        user = get_object_or_404(User, username=username)
        experience = get_list_or_404(WorkExperience, user=user)
        education = get_list_or_404(Education, user=user)
        profile_img = get_object_or_404(UserProfile, user=user)
    except:
        pass

    context = {
        'experiences': experience,
        'educations': education,
        'profile_img': profile_img,
    }

    template = 'profiles/selected_user_profile.html'
    return render(request, template, context)


class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm


class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm