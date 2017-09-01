from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView

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

from .forms import QuestForm, QuestImageForm
from .models import Quest, UserProfile, Upload

# Create your views here.

@login_required
def get_user_settings(request):
    profile_user = get_object_or_404(User, username=request.user.username)
    profile_thumbnail = get_object_or_404(UserProfile, user=request.user)
    verified = get_object_or_404(EmailAddress, user=request.user, primary="True")
    context = {
        'profile_user': profile_user,
        'profile_img': profile_thumbnail,
        'verification': verified,
    }
    return render(request, 'account/user_settings.html', context)


@login_required
def user_dashboard(request):
    template_name = 'account/user_dashboard.html'
    return render(request, template_name, {})


@login_required
def user_quest_list_view(request):
    initial_list = [''] * 3
    user_quest_list, active_list, exploded_list = initial_list
    try:
        user_quest_list = Quest.objects.filter(user=request.user)
        active_list = user_quest_list.filter(explosion_datetime__lte=timezone.now())
        exploded_list = user_quest_list.filter(explosion_datetime__gte=timezone.now())
    except ObjectDoesNotExist:
        msg = "No quest"
        raise ObjectDoesNotExist(msg)
    context = {
        'list': user_quest_list,
        'actives': active_list,
        'exploded': exploded_list,
    }
    return render(request, 'account/user_quest_list.html', context)


def get_selected_user_list(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)

    user_quests_list = ''
    try:
        user_quests_list = get_list_or_404(Quest, user=user)
    except ObjectDoesNotExist:
        pass

    context = {
        'user': user,
        'profile': profile,
        'user_quests_list': user_quests_list,
    }

    template = 'quests/selected_user_list.html'
    return render(request, template, context)


class PasswordChangePageView(PasswordChangeView):
    @property
    def success_url(self):
        return reverse_lazy("user_profile")

password_change_page_view = login_required(PasswordChangePageView.as_view())


@login_required
def edit_quest_images(request, slug):
    quest = get_object_or_404(Quest, slug=slug)

    if quest.user != request.user:
        raise Http404
    
    form_class = QuestImageForm 

    if request.method == "POST":
        form = form_class(
            data=request.POST,
            files=request.FILES,
            instance=quest)
        
        files = request.FILES.getlist('image')

        if form.is_valid():
            for f in files:
                Upload.objects.create(
                    quest=quest,
                    image=f,)
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
    upload = get_object_or_404(Upload, id=id)

    if upload.quest.user != request.user:
        raise Http404

    upload.delete()

    return redirect('quests:edit_quest_images', slug=upload.quest.slug)


@login_required
def upload_profile_images(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.user != user_profile.user:
        raise Http404

    form_class = UploadProfileForm

    if request.method == "POST":
        form = form_class(
            data=request.POST,
            files=request.FILES,
            instance=user_profile)

        if form.is_valid():
            UserProfile.object.create(
                user=current_user,
                profile_image=form.cleaned_data['profile_image'],
                location=None,)

        return redirect('homepage')

    else:
        form = form_class(instance=user_profile)

    context = {
        'profile': user_profile,
        'form': form,
    }

    return render(request, 'accounts/user_profile.html', context)


class DiffuseToggle(LoginRequiredMixin, RedirectView):
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
                        'Diffuse message successfully sent to the quest creator',
                        extra_tags='diffuse-message')
                    obj.interested_users.add(user)
                else:
                    pass
            else:
                if user != obj.user:
                    messages.success(
                        request,
                        'Diffuse message retracted',
                        extra_tags='diffuse-message')
                    obj.interested_users.remove(user)
                else:
                    pass
        return url_


class QuestListView(ListView):
    template_name = "index.html"
    context_object_name = 'quest_list'
    model = Quest

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['thumbnails'] = Upload.objects.first()
        return context

    def get_queryset(self):
        still_ticking = Quest.objects.all().exclude(explosion_datetime__lte=timezone.now())
        query = self.request.GET.get('q')
        if query:
            # still_ticking = still_ticking.filter()
            # results = Quest.objects.filter(explosion_datetime__gte=timezone.now())
            results = still_ticking.filter(
                Q(title__icontains=query) | Q(description__icontains=query))
            return results
        else:
            return still_ticking


class QuestDetailView(DetailView):
    template_name = 'quests/quest_detail.html'
    context_object_name = 'quest'
    model = Quest

    def get_context_data(self, *args, **kwargs):
        context = super(QuestDetailView, self).get_context_data(*args, **kwargs)
        selected_quest = get_object_or_404(Quest, slug=self.kwargs['slug'])
        user = get_object_or_404(User, quests__slug=self.kwargs['slug'])
        context['profile_picture'] = get_object_or_404(UserProfile, user=user)
        context['uploaded_images'] = selected_quest.uploads.all() 
        return context


class CreateQuest(LoginRequiredMixin, CreateView):
    model = Quest
    form_class = QuestForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateQuestView(LoginRequiredMixin, UpdateView):
    model = Quest
    form_class = QuestForm


class DeleteQuestView(LoginRequiredMixin, DeleteView):
    template_name = 'quests/delete_quest.html'
    model = Quest
    success_url = reverse_lazy('homepage')
