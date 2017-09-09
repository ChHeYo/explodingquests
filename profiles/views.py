from allauth.account.models import EmailAddress

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic import (
    CreateView, ListView, 
    UpdateView, DeleteView, 
    DetailView, RedirectView,)
from django.utils import timezone

from quests.models import UserProfileImage, Quest

from .models import Education, WorkExperience, DefuseMessage
from .forms import EducationForm, WorkExperienceForm, SendMessageForm

# Create your views here.


@login_required
def profile_list_view(request):
    """A page where users can view their own profile"""
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
    """A page where users can view their collection of quests"""
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
    """User dashboard"""
    profile_pic = UserProfileImage.objects.get(user=request.user)
    template_name = 'profiles/user_dashboard.html'
    context = {
        'profile_pic': profile_pic,
    }
    return render(request, template_name, context)


class MessageInboxView(LoginRequiredMixin, ListView):
    """Message Inbox page"""
    model = DefuseMessage
    context_object_name = 'messages'
    template_name = 'profiles/inbox_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['receiver'] = DefuseMessage.objects.filter(
            receiver=self.request.user, trash_by_receiver=False).order_by('-send_at')
        context['sender'] = DefuseMessage.objects.filter(
            sender=self.request.user, trash_by_sender=False).order_by('-send_at')
        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    """message detail"""
    model = DefuseMessage
    context_object_name = 'message'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        particular_message = get_object_or_404(DefuseMessage, pk=self.kwargs['pk'])
        context['sender_email'] = get_object_or_404(EmailAddress, user=particular_message.sender)
        context['sender_profile'] = get_object_or_404(UserProfileImage, user=particular_message.sender)
        context['quest'] = get_object_or_404(Quest, slug=particular_message.related_quest.slug)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        current_user = get_object_or_404(User, username=self.request.user.username)
        if self.object.receiver == current_user:
            self.object.read_by_receiver()
            print('read')
        return self.render_to_response(context)


class MessageDelete(LoginRequiredMixin, RedirectView):
    """delete message button"""
    def get_redirect_url(self, *args, **kwargs):
        msg_pk = self.kwargs.get('pk')
        msg = get_object_or_404(DefuseMessage, pk=msg_pk)
        msg_sender = get_object_or_404(User, username=msg.sender.username)
        msg_receiver = get_object_or_404(User, username=msg.receiver.username)
        url_ = reverse_lazy("dashboard:message_inbox")
        user = self.request.user
        if user.is_authenticated():
            if msg_sender == user:
                if not msg.trash_by_sender:
                    msg.trash_by_sender = True
                    msg.save()
                else:
                    pass
            elif msg.receiver == user:
                if not msg.trash_by_receiver:
                    msg.trash_by_receiver = True
                    msg.save()
                else:
                    pass
            else:
                pass
        return url_


class WorkExperienceCreateView(LoginRequiredMixin, CreateView):
    """adding experience to profile"""
    model = WorkExperience
    form_class = WorkExperienceForm
    success_url = reverse_lazy("dashboard:my_profile")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class WorkExperienceUpdateView(LoginRequiredMixin, UpdateView):
    """updating an experience"""
    model = WorkExperience
    form_class = WorkExperienceForm


class WorkExperienceDeleteView(LoginRequiredMixin, DeleteView):
    """deleting an experience"""
    model = WorkExperience
    template_name = 'profiles/delete_experience.html'
    success_url = reverse_lazy('dashboard:my_profile')
