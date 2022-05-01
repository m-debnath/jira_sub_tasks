from django.contrib import admin
from .models import *

admin.site.register(JIRA)
admin.site.register(JIRAUsers)
admin.site.register(DevTasks)
admin.site.register(TestTasks)
admin.site.register(AnalysisTasks)
admin.site.register(FieldMapping)
admin.site.register(DevDOR)
admin.site.register(DevDOD)
admin.site.register(JIRALabel)
admin.site.register(JiraApp)
admin.site.register(AppInfo)
admin.site.register(Backlog)
admin.site.register(Team)
admin.site.register(JiraStatus)
