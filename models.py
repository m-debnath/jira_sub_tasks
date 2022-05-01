from django.db import models


class JIRA(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return "Name: " + self.name + ", Value: " + self.value


class JIRAUsers(models.Model):
    key = models.CharField(max_length=30)
    displayName = models.CharField(max_length=150)
    role = models.CharField(max_length=30, null=True, blank=True)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Name: " + self.displayName + ", Login: " + self.key + ", Role: " + self.role + ", Team: " + self.team


class DevTasks(models.Model):
    type = models.CharField(max_length=50)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    jteam = models.CharField(max_length=50, null=True, blank=True)
    application = models.CharField(max_length=50)
    hours = models.CharField(max_length=10, null=True, blank=True)
    hoursDesc = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Summary: " + self.summary + ", Team: " + self.team


class TestTasks(models.Model):
    type = models.CharField(max_length=50)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    jteam = models.CharField(max_length=50, null=True, blank=True)
    application = models.CharField(max_length=50)
    hours = models.CharField(max_length=10, null=True, blank=True)
    hoursDesc = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Summary: " + self.summary + ", Team: " + self.team


class AnalysisTasks(models.Model):
    type = models.CharField(max_length=50)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    jteam = models.CharField(max_length=50, null=True, blank=True)
    application = models.CharField(max_length=50)
    hours = models.CharField(max_length=10, null=True, blank=True)
    hoursDesc = models.CharField(max_length=100, null=True, blank=True)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Summary: " + self.summary + ", Team: " + self.team


class FieldMapping(models.Model):
    appname = models.CharField(max_length=50)
    jiraname = models.CharField(max_length=50)

    def __str__(self):
        return "Name: " + self.appname + ", JIRA Name: " + self.jiraname


class DevDOR(models.Model):
    name = models.CharField(max_length=250)
    checked = models.CharField(max_length=10)
    option = models.CharField(max_length=10)
    id_1 = models.CharField(max_length=10)
    rank = models.CharField(max_length=10)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Name: " + self.name + ", Team: " + self.team


class DevDOD(models.Model):
    name = models.CharField(max_length=250)
    checked = models.CharField(max_length=10)
    option = models.CharField(max_length=10)
    id_1 = models.CharField(max_length=10)
    rank = models.CharField(max_length=10)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Name: " + self.name + ", Team: " + self.team


class JIRALabel(models.Model):
    type = models.CharField(max_length=50)
    jiraLabel = models.CharField(max_length=50)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Type: " + self.type + ", JIRA Label: " + self.jiraLabel + ", Team: " + self.team


class JiraApp(models.Model):
    AppName = models.CharField(max_length=20)
    AppDesc = models.CharField(max_length=50)
    AppHomeUrl = models.CharField(max_length=100)
    AppHomeTooltip = models.CharField(max_length=50, null=True, blank=True)
    AppId = models.CharField(max_length=10)
    AppDashUrl = models.CharField(max_length=250)
    AppDashTooltip = models.CharField(max_length=50, null=True, blank=True)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Name: " + self.AppName + ", Description: " + self.AppDesc + ", Team: " + self.team


class AppInfo(models.Model):
    key = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __str__(self):
        return "Name: " + self.key + ", Value: " + self.value


class Backlog(models.Model):
    desc = models.CharField(max_length=250)

    def __str__(self):
        return "Description: " + self.desc


class Team(models.Model):
    key = models.CharField(max_length=30)
    jira_id = models.CharField(max_length=30)
    jira_desc = models.CharField(max_length=100)
    jira_app_id = models.CharField(max_length=30, null=True, blank=True)
    jira_app_desc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Key: " + self.key + ", Name: " + self.jira_desc


class JiraStatus(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    team = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "Key: " + self.key + ", Value: " + self.value + ", Team: " + self.team
