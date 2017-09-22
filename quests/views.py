from allauth.account.models import EmailAddress
from allauth.account.views import (
    PasswordChangeView, AccountInactiveView,
    EmailVerificationSentView, PasswordResetView, )

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import (
    render, Http404,
    get_object_or_404,
    get_list_or_404,
    HttpResponse,
    redirect,
)
from django.utils import timezone
from django.views.generic import (
    TemplateView, ListView, DetailView,
    RedirectView,
)
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView,
)

from profiles.models import WorkExperience, Education, DefuseMessage
from profiles.forms import SendMessageForm

from .forms import QuestForm, QuestImageForm, ProfileImageForm
from .models import Quest, UserProfileImage, Upload
from .mixins import RightfulOwnerOfQuestMixin, SendingPermissionMixin

# Create your views here.


@login_required
def get_user_settings(request):
    """go to user settings"""
    profile_user = get_object_or_404(User, username=request.user.username)
    user_profile = UserProfileImage.objects.get(user=profile_user)
    verified = get_object_or_404(EmailAddress, user=request.user, primary=True)

    if request.user != user_profile.user:
        raise Http404

    form_class = ProfileImageForm

    if request.method == "POST":
        form = form_class(
            data=request.POST,
            files=request.FILES,
            instance=user_profile)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = profile_user
            obj.profile_thumbnail = form.cleaned_data['profile_thumbnail']
            obj.save()

        return redirect('user_settings')

    else:
        form = form_class(instance=user_profile)

    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'verification': verified,
        'profile_img_form': form,
    }
    return render(request, 'account/user_settings.html', context)


def get_selected_user_list(request, username):
    """get quests posted by this user"""
    user = get_object_or_404(User, username=username)
    profile = UserProfileImage.objects.get(user=user) 
    verified = get_object_or_404(EmailAddress, user=user, primary="True")

    user_quests_list = ''
    try:
        user_quests_list = get_list_or_404(Quest, user=user, explosion_datetime__gte=timezone.now())
    except ObjectDoesNotExist:
        pass

    context = {
        'user': user,
        'profile': profile,
        'user_quests_list': user_quests_list,
        'verified': verified,
    }

    template = 'quests/selected_user_list.html'
    return render(request, template, context)


class PasswordChangePageView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy("user_settings")

password_change_page_view = login_required(PasswordChangePageView.as_view())


class AccountInactiveViewRedux(LoginRequiredMixin, AccountInactiveView):
    @property
    def template_name(self):
        if self.request.user.is_active:
            raise Http404
        return 'account/account_inactive.html'

account_inactive_redux = login_required(AccountInactiveViewRedux.as_view())


class EmailVerificationSentViewRedux(LoginRequiredMixin, EmailVerificationSentView):
    @property
    def template_name(self):
        raise Http404

email_verification_redux = login_required(EmailVerificationSentViewRedux.as_view())


@login_required
def edit_quest_images(request, slug):
    """add quest image"""
    quest = get_object_or_404(Quest, slug=slug)

    if quest.user != request.user:
        raise Http404
    
    form_class = QuestImageForm

    if request.method == "POST":
        form = form_class(
            data=request.POST,
            files=request.FILES,
            instance=quest)
        
        files = request.FILES.getlist('quest_images')

        if form.is_valid():
            for f in files:
                Upload.objects.create(
                    quest=quest,
                    quest_images=f,)
        return redirect('quests:quest_detail', slug=slug)

    else:
        form = form_class(instance=quest)

    uploads = quest.uploads.all()

    context = {
        'quest': quest,
        'image_form': form,
        'uploads': uploads,
    }

    return render(request, 'quests/edit_quest_images.html', context)


@login_required
def delete_quest_images(request, id):
    """delete quest image"""
    upload = get_object_or_404(Upload, id=id)

    if request.user != upload.quest.user:
        raise Http404

    upload.delete()

    return redirect('quests:edit_quest_images', slug=upload.quest.slug)


@login_required
def interested_users_list(request, slug):
    """go to defuse list for a particular quest"""
    selected_quest = get_object_or_404(Quest, slug=slug)
    interested_users = selected_quest.interested_users.all()

    if request.user != selected_quest.user:
        raise Http404

    context = {
        'interested_users': interested_users,
        'selected_quest': selected_quest,
    }
    return render(request, 'quests/interested_users.html', context)


@login_required
def get_selected_user_profile(request, slug, username):
    """go to a particular user profile page who pressed defuse for this quest"""
    user = get_object_or_404(User, username=username)
    quest = get_object_or_404(Quest, slug=slug)
    profile_img = UserProfileImage.objects.get(user=user)

    experience = ''

    if request.user != quest.user:
        raise Http404
    else:
        if user not in quest.interested_users.all():
            raise Http404

    try:
        email = get_object_or_404(EmailAddress, user=user, primary=True)
        experience = get_list_or_404(WorkExperience, user=user)
    except:
        pass

    context = {
        'user': user,
        'email': email,
        'experiences': experience,
        'profile_img': profile_img,
        'quest': quest,
    }

    template = 'quests/selected_user_profile.html'
    return render(request, template, context)


class MessageCreateView(LoginRequiredMixin, SendingPermissionMixin, CreateView):
    """creating messages"""
    model = DefuseMessage
    form_class = SendMessageForm
    template_name = 'quests/send_message_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        receiver = get_object_or_404(User, username=self.kwargs['username']) 
        context['quest'] = get_object_or_404(Quest, slug=self.kwargs['slug'])
        context['sender'] = get_object_or_404(User, username=self.request.user.username)
        context['receiver_email'] = get_object_or_404(EmailAddress, user=receiver)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.receiver = User.objects.get(username=self.kwargs['username'])
        self.object.related_quest = Quest.objects.get(slug=self.kwargs['slug'])
        self.object.parent = None
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("quests:interested_users", kwargs={'slug': self.kwargs['slug']})


class DiffuseToggle(LoginRequiredMixin, RedirectView):
    """for taking care of logics of pressing defuse"""
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Quest, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        request = self.request
        if user.is_authenticated():
            if user not in obj.interested_users.all():
                if user != obj.user:
                    messages.success(
                        request,
                        'Diffuse message successfully sent. The quest creator can now access your profile info.',
                        extra_tags='diffuse-message')
                    obj.interested_users.add(user)
                else:
                    pass
            else:
                if user != obj.user:
                    messages.success(
                        request,
                        'Diffuse message retracted. Your profile info will now be inaccessible to the quest creator.',
                        extra_tags='diffuse-message')
                    obj.interested_users.remove(user)
                else:
                    pass
        return url_


class QuestListView(ListView):
    """Get the total list of quests"""
    template_name = "index.html"
    context_object_name = 'quest_list'
    model = Quest

    def get_queryset(self):
        still_ticking = Quest.objects.all().exclude(explosion_datetime__lte=timezone.now())
        query = self.request.GET.get('q')
        if query:
            results = still_ticking.filter(
                Q(title__icontains=query) | Q(description__icontains=query))
            return results
        else:
            return still_ticking


class QuestDetailView(DetailView):
    """go to detail page of a particular quest"""
    template_name = 'quests/quest_detail.html'
    context_object_name = 'quest'
    model = Quest

    def get_context_data(self, *args, **kwargs):
        context = super(QuestDetailView, self).get_context_data(*args, **kwargs)
        selected_quest = get_object_or_404(Quest, slug=self.kwargs['slug'])
        user = get_object_or_404(User, quests__slug=self.kwargs['slug'])
        context['profile_picture'] = UserProfileImage.objects.get(user=user)
        context['uploaded_images'] = selected_quest.uploads.all()
        context['interested_users_list'] = selected_quest.interested_users.all()
        return context


class CreateQuest(LoginRequiredMixin, CreateView):
    """take the user to the quest creation page"""
    model = Quest
    form_class = QuestForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateQuestView(LoginRequiredMixin, RightfulOwnerOfQuestMixin, UpdateView):
    """updating quest"""
    template_name = 'quests/quest_update_form.html'
    model = Quest
    form_class = QuestForm

    def get_context_data(self, *args, **kwargs):
        '''just to be on the safe side'''
        context = super().get_context_data(*args, **kwargs)
        current_quest = get_object_or_404(Quest, slug=self.kwargs['slug'])
        context['current_user'] = get_object_or_404(User, username=self.request.user)
        context['quest_creator'] = get_object_or_404(User, username=current_quest.user.username)
        return context


class DeleteQuestView(LoginRequiredMixin, RightfulOwnerOfQuestMixin, DeleteView):
    """deleting quest"""
    template_name = 'quests/delete_quest.html'
    model = Quest
    success_url = reverse_lazy('homepage')

    def get_context_data(self, *args, **kwargs):
        '''just to be on the safe side'''
        context = super().get_context_data(*args, **kwargs)
        current_quest = get_object_or_404(Quest, slug=self.kwargs['slug'])
        context['current_user'] = get_object_or_404(User, username=self.request.user)
        context['quest_creator'] = get_object_or_404(User, username=current_quest.user.username)
        return context
