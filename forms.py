from django import forms
from django.contrib.auth.forms import AuthenticationForm
from jira import JIRA
from jira.exceptions import JIRAError
from .models import JIRA as JIRAModel
from .models import Team
from django.conf import settings
import os


class UserLoginForm(AuthenticationForm):
    CHOICES = ()
    teams = Team.objects.all()
    for team in teams:
        CHOICES = CHOICES + ((team.key, team.jira_desc),)
    select_team = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

    def confirm_login_allowed(self, user):
        pass

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        jira_cert = os.path.join(settings.STATIC_ROOT, 'jira_sub_tasks/jira_cert.cer')

        if username and password:
            try:
                jira_options = {
                    'server': JIRAModel.objects.filter(name='server').first().value,
                    'verify': jira_cert,
                }
                JIRA(basic_auth=(username, password), options=jira_options, max_retries=0)
            except JIRAError as e:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data
