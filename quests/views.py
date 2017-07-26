from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
)
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView,
)

from .models import Quest, UserProfile

# Create your views here.


class HomePageTemplateView(TemplateView):
    template_name = 'index.html'


def get_user_profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/user_profile.html', {'user': user})

# class UserProfileView(DetailView):
#     template_name = 'account/user_profile.html'
#     model = UserProfile


class QuestListView(ListView):
    template_name = "index.html"
    model = Quest


class QuestDetailView(DetailView):
    template_name = 'quests/quest_detail.html'
    model = Quest


class CreateQuest(LoginRequiredMixin, CreateView):
    model = Quest
    fields = ['title', 'description', 'reward_type', 'rewards', 'explosion_date']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.npc = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateQuestView(LoginRequiredMixin, UpdateView):
    fields = ('title', 'description', 'rewards')
    model = Quest


class DeleteQuestView(LoginRequiredMixin, DeleteView):
    template_name = 'quests/delete_quest.html'
    model = Quest
    success_url = reverse_lazy('homepage')