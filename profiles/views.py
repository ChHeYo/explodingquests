from allauth.account.models import EmailAddress

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.utils import timezone

from quests.models import UserProfileImage, Quest

from .models import Education, WorkExperience, DefuseMessage
from .forms import EducationForm, WorkExperienceForm, SendMessageForm

# Create your views here.


@login_required
def profile_list_view(request):
    
    user = get_object_or_404(User, username=request.user.username)
    email = get_object_or_404(EmailAddress, user=user, primary=True)
    profile_img = get_object_or_404(UserProfileImage, user=user)
    experience = ''
    
    try:
        experience = get_list_or_404(WorkExperience, user=user)
    except: 
        pass

    context = {
        'user': user,
        'email': email,
        'experiences': experience,
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
    except ObjectDoesNotExist:
        msg = "No quest"
        raise ObjectDoesNotExist(msg)
    context = {
        'list': user_quest_list,
        'count': user_quest_list_count,
        'def_quests': defused_quests,
        'def_quest_count': defused_quests_count,
    }
    return render(request, 'profiles/user_quest_list.html', context)


@login_required
def user_dashboard(request):
    profile_pic = UserProfileImage.objects.get(user=request.user)
    template_name = 'profiles/user_dashboard.html'
    context = {
        'profile_pic': profile_pic,
    }
    return render(request, template_name, context)


# @login_required
# def get_selected_user_profile(request, username):
    
#     user = get_object_or_404(User, username=username)
#     profile_img = UserProfileImage.objects.get(user=user)

#     experience = ''

#     try:
#         email = get_object_or_404(EmailAddress, user=user, primary=True)
#         experience = get_list_or_404(WorkExperience, user=user)
#     except:
#         pass

#     context = {
#         'user': user,
#         'email': email,
#         'experiences': experience,
#         'profile_img': profile_img,
#     }

#     template = 'profiles/selected_user_profile.html'
#     return render(request, template, context)


class MessageInboxView(LoginRequiredMixin, ListView):
    model = DefuseMessage
    context_object_name = 'messages'
    template_name = 'profiles/inbox_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['receiver'] = DefuseMessage.objects.filter(receiver=self.request.user)
        context['sender'] = DefuseMessage.objects.filter(sender=self.request.user).order_by('-send_at')
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = DefuseMessage
    context_object_name = 'message'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        particular_message = get_object_or_404(DefuseMessage, pk=self.kwargs['pk'])
        context['sender_email'] = get_object_or_404(EmailAddress, user=particular_message.sender)
        context['sender_profile'] = get_object_or_404(UserProfileImage, user=particular_message.sender)
        return context


class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    success_url = reverse_lazy("dashboard:my_profile")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class WorkExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkExperience
    form_class = WorkExperienceForm


class WorkExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkExperience
    template_name = 'profiles/delete_experience.html'
    success_url = reverse_lazy('dashboard:my_profile')
