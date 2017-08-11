from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import (
    render, Http404,
    get_object_or_404,
    get_list_or_404,
)
from django.utils import timezone
from django.views.generic import (
    TemplateView, ListView, DetailView,
)
from django.views.generic.edit import (
    CreateView, DeleteView, UpdateView,
)

from .forms import QuestForm
from .models import Quest, UserProfile, Upload

# Create your views here.


class HomePageTemplateView(TemplateView):
    template_name = 'index.html'


def get_user_profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/user_profile.html', {'user': user})


@login_required
def user_quest_list_view(request):
    user_quest_list = ''
    active_list = ''
    exploded_list = ''
    try:
        user_quest_list = Quest.objects.filter(user=request.user)
        # active_list = Quest.objects.filter(user=request.user).filter(explosion_date__lte=timezone.now())
        # exploded_list = Quest.objects.filter(user=request.user).filter(explosion_date__gte=timezone.now())
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


# @login_required
# def upload_quest_images(request, slug):
#     thing = get_object_or_404(Quest, slug=slug)

#     if thing.user != request.user:
#         raise Http404
    
#     form_class = QuestForm

#     if request.method == "POST":
#         form = form_class(data=request.POST, files=request.FILES, instance=thing)

#         if form.is_valid():
#             Upload.objects.create(image=form.cleaned_data.get['image'], quest=thing)

#         return redirect('upload_quest_images', slug=slug)

#     else:
#         form = form_class(instance=quest)


class QuestListView(ListView):
    template_name = "index.html"
    context_object_name = 'quest_list'
    model = Quest
    queryset = Quest.objects.all().exclude(explosion_datetime__lte=timezone.now())


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
