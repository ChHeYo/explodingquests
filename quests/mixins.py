from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, Http404

from .models import Quest


class RightfulOwnerOfQuestMixin(object):
    """Checking if request user is the same as quest creator"""
    def get_template_names(self):
        quest = get_object_or_404(Quest, slug=self.kwargs['slug'])
        quest_creator = get_object_or_404(User, username=quest.user.username)
        if self.template_name is None:
            raise ImproperlyConfigured(
            "TemplateResponseMixin requires either a definition of "
            "'template_name' or an implementation of 'get_template_names()'")
        else:
            if self.request.user != quest_creator:
                raise Http404
            else:
                return [self.template_name]


class SendingPermissionMixin(object):
    """Ensure that messages can only to sent to users in interested list"""
    def get_template_names(self):
        quest = get_object_or_404(Quest, slug=self.kwargs['slug'])
        quest_creator = get_object_or_404(User, username=quest.user.username)
        receiver = get_object_or_404(User, username=self.kwargs['username'])
        if self.template_name is None:
            raise ImproperlyConfigured(
            "TemplateResponseMixin requires either a definition of "
            "'template_name' or an implementation of 'get_template_names()'")
        else:
            if self.request.user != quest_creator:
                raise Http404
            else:
                if receiver not in quest.interested_users.all():
                    raise Http404
            return [self.template_name]