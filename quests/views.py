from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404, get_object_or_404, get_list_or_404
from django.views.generic import (
    TemplateView, ListView, DetailView,
)
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView,
)

from .forms import QuestForm
from .models import Quest, UserProfile

# Create your views here.


class HomePageTemplateView(TemplateView):
    template_name = 'index.html'


def get_user_profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/user_profile.html', {'user': user})


@login_required
def user_quest_list_view(request):
    user_quest_list = ''
    try:
        user_quest_list = Quest.objects.filter(user=request.user)
    except ObjectDoesNotExist: 
        msg = "No quest"
        raise ObjectDoesNotExist(msg)
    return render(request, 'account/user_quest_list.html', {'list': user_quest_list})


def get_selected_user_list(request, username):
    user = get_object_or_404(User, username=username)
    # user = User.objects.get(username=username)
    profile = get_object_or_404(UserProfile, username=user)
    # profile = UserProfile.objects.get(username=username)
    
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


class QuestListView(ListView):
    template_name = "index.html"
    context_object_name = 'quest_list'
    model = Quest
    queryset = Quest.objects.filter(status='Ticking')


class QuestDetailView(DetailView):
    template_name = 'quests/quest_detail.html'
    context_object_name = 'quest'
    model = Quest

    def get_context_data(self, *args, **kwargs):
        context = super(QuestDetailView, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, quests__slug=self.kwargs['slug'])
        context['profile_picture'] = get_object_or_404(UserProfile, username=user)
        return context


class CreateQuest(LoginRequiredMixin, CreateView):
    form_class = QuestForm
    model = Quest
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateQuestView(LoginRequiredMixin, UpdateView):
    fields = ('title', 'description', 'rewards')
    model = Quest


class DeleteQuestView(LoginRequiredMixin, DeleteView):
    template_name = 'quests/delete_quest.html'
    model = Quest
    success_url = reverse_lazy('homepage')
