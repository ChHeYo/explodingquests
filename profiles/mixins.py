from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, Http404

from .models import DefuseMessage, WorkExperience

class CheckingUserPermissionMixin(object):
    """Checking user permission"""
    def get_template_names(self):
        particular_defuse_msg = get_object_or_404(DefuseMessage, pk=self.kwargs['pk'])
        currently_loggedin = get_object_or_404(User, username=self.request.user)
        msg_sender = get_object_or_404(User, username=particular_defuse_msg.sender.username)
        msg_receiver = get_object_or_404(User, username=particular_defuse_msg.receiver.username)
        sender_and_receiver = (msg_sender, msg_receiver)
        if self.template_name is None:
            raise ImproperlyConfigured(
            "TemplateResponseMixin requires either a definition of "
            "'template_name' or an implementation of 'get_template_names()'")
        else:
            if currently_loggedin not in sender_and_receiver:
                raise Http404
            else:
                return [self.template_name]


class UserExperiencePermissionMixin(object):
    """Updating and deleting experience permission"""
    def get_template_names(self):
        currently_loggedin = get_object_or_404(User, username=self.request.user)
        particular_experience = get_object_or_404(WorkExperience, pk=self.kwargs['pk'])
        particular_experience_user = get_object_or_404(User, username=particular_experience.user.username)
        if self.template_name is None:
            raise ImproperlyConfigured(
            "TemplateResponseMixin requires either a definition of "
            "'template_name' or an implementation of 'get_template_names()'")
        else:
            if currently_loggedin != particular_experience_user:
                raise Http404
            else:
                return [self.template_name] 