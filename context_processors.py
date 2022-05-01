from .models import JiraApp, AppInfo, Team
from django.contrib.auth.models import User


def jiraapp(request):
    jiraapps = JiraApp.objects.all()
    appinfos = AppInfo.objects.all()
    teams = Team.objects.all()
    return {'jiraapps': jiraapps, 'appinfos': appinfos, 'teams': teams}
