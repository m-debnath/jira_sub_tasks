from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from jira import JIRA
from jira.exceptions import JIRAError
from .forms import UserLoginForm
from .models import JIRA as JIRAModel
from .models import JIRAUsers, JIRALabel, DevTasks, TestTasks, AnalysisTasks, JiraApp, Backlog
import re
from django.conf import settings
import os


def home(request):
    sprintpat = re.compile(r"name=[^,]*,")

    try:
        username = request.session['username']
        password = request.session['password']
        team = request.session['team']
        jiraapp = JiraApp.objects.filter(team=team).first()
        if team == 'PLAT':
            ANA_LABEL = JIRALabel.objects.filter(Q(type="Analysis") & Q(team=team)).first().jiraLabel
            DEV_LABEL = JIRALabel.objects.filter(Q(type="Implementation") & Q(team=team)).first().jiraLabel
            TEST_LABEL = JIRALabel.objects.filter(Q(type="Testing") & Q(team=team)).first().jiraLabel
        elif team == 'BWB':
            ANA_LABELS = JIRALabel.objects.filter(Q(type="Analysis") & Q(team=team))
            DEV_LABELS = JIRALabel.objects.filter(Q(type="Implementation") & Q(team=team))
            BUG_LABELS = JIRALabel.objects.filter(Q(type="Bug Fix") & Q(team=team))
            CONFIG_LABELS = JIRALabel.objects.filter(Q(type="Configuration") & Q(team=team))
            DEV_CONFIG_LABELS = JIRALabel.objects.filter(Q(type="Implementation_Configuration") & Q(team=team))

        userDispName = JIRAUsers.objects.filter(key=username).first().displayName
        devusers = JIRAUsers.objects.filter(Q(team=team)).filter(Q(role="Developer") | Q(role="Analyst") | Q(role="Scrum Master"))
        testusers = JIRAUsers.objects.filter(Q(team=team)).filter(Q(role="Tester") | Q(role="Scrum Master"))
        anausers = JIRAUsers.objects.filter(Q(team=team)).filter(Q(role="Analyst") | Q(role="Scrum Master"))
        try:
            jira_cert = os.path.join(settings.STATIC_ROOT, 'jira_sub_tasks/jira_cert.cer')
            jira_options = {
                'server': JIRAModel.objects.filter(name='server').first().value,
                'verify': jira_cert,
            }
            jira = JIRA(basic_auth=(username, password), options=jira_options, max_retries=0)
        except JIRAError:
            return redirect('login')
        if request.method == 'POST':
            story_number = request.POST.get('story_number', '')
            final_story_number = ''
            dev_tasks = []
            test_tasks = []
            ana_tasks = []
            if story_number == '':
                final_story_number = request.POST.get('input_story_number', '')
                story_number = final_story_number

            if story_number != '':
                try:
                    story = jira.issue(story_number)
                    labels = story.fields.labels
                    status = str(story.fields.status)

                    status = status.replace('Story: ', '')
                    sprintName = ""
                    try:
                        sprintName = sprintpat.findall(str(story.fields.customfield_10005))[0]
                        sprintName = sprintName[5:-1]
                    except IndexError:
                        pass
                    story_type = ""
                    dev_display = "none"
                    test_display = "none"
                    ana_display = "none"
                    if team == 'PLAT':
                        dev_tasks = DevTasks.objects.filter(Q(team=team))
                        test_tasks = TestTasks.objects.filter(Q(team=team))
                        ana_tasks = AnalysisTasks.objects.filter(Q(team=team))
                        if ANA_LABEL in labels and DEV_LABEL in labels:
                            story_type = "AnalysisDevelopment"
                            dev_display = "block"
                            test_display = "block"
                            ana_display = "block"
                        elif ANA_LABEL in labels:
                            story_type = "Analysis"
                            dev_display = "none"
                            test_display = "none"
                            ana_display = "block"
                        elif DEV_LABEL in labels:
                            story_type = "Development"
                            dev_display = "block"
                            test_display = "block"
                            ana_display = "none"
                        elif TEST_LABEL in labels:
                            story_type = "Testing"
                            dev_display = "none"
                            test_display = "block"
                            ana_display = "none"
                    elif team == 'BWB':
                        for ANA_LABEL in ANA_LABELS:
                            if ANA_LABEL.jiraLabel in labels:
                                story_type = "Analysis"
                                dev_display = "none"
                                test_display = "none"
                                ana_display = "block"
                                ana_tasks = AnalysisTasks.objects.filter(Q(team=team))
                                dev_tasks = DevTasks.objects.filter(Q(team=team))
                                test_tasks = TestTasks.objects.filter(Q(team=team))
                        for BUG_LABEL in BUG_LABELS:
                            if BUG_LABEL.jiraLabel in labels:
                                story_type = "BugFix"
                                dev_display = "block"
                                test_display = "block"
                                ana_display = "none"
                                ana_tasks = AnalysisTasks.objects.filter(Q(team=team))
                                dev_tasks = DevTasks.objects.filter(Q(team=team)).filter(Q(type="Tele2 Technical Sub-Task") | Q(type="Tele2 Test Sub-Task") | Q(type="Tele2 General Sub-Task"))
                                test_tasks = TestTasks.objects.filter(Q(team=team))
                        for CONFIG_LABEL in CONFIG_LABELS:
                            if CONFIG_LABEL.jiraLabel in labels:
                                story_type = "Configuration"
                                dev_display = "block"
                                test_display = "block"
                                ana_display = "none"
                                ana_tasks = AnalysisTasks.objects.filter(Q(team=team))
                                dev_tasks = DevTasks.objects.filter(Q(team=team)).filter(Q(type="Tele2 Configuration Sub-Task") | Q(type="Tele2 Test Sub-Task") | Q(type="Tele2 General Sub-Task"))
                                test_tasks = TestTasks.objects.filter(Q(team=team))
                        for DEV_LABEL in DEV_LABELS:
                            if DEV_LABEL.jiraLabel in labels:
                                story_type = "Development"
                                dev_display = "block"
                                test_display = "block"
                                ana_display = "none"
                                ana_tasks = AnalysisTasks.objects.filter(Q(team=team))
                                dev_tasks = DevTasks.objects.filter(Q(team=team)).filter(Q(type="Tele2 Development Sub-Task") | Q(type="Tele2 Test Sub-Task") | Q(type="Tele2 General Sub-Task"))
                                test_tasks = TestTasks.objects.filter(Q(team=team))
                        for DEV_CONFIG_LABEL in DEV_CONFIG_LABELS:
                            if DEV_CONFIG_LABEL.jiraLabel in labels:
                                story_type = "Implementation_Configuration"
                                dev_display = "block"
                                test_display = "block"
                                ana_display = "none"
                                ana_tasks = AnalysisTasks.objects.filter(Q(team=team))
                                dev_tasks = DevTasks.objects.filter(Q(team=team)).filter(Q(type="Tele2 Development Sub-Task") | Q(type="Tele2 Configuration Sub-Task") | Q(type="Tele2 Test Sub-Task") | Q(type="Tele2 General Sub-Task"))
                                test_tasks = TestTasks.objects.filter(Q(team=team))

                    if final_story_number != '':
                        # proceed to create sub-tasks
                        # development inputs
                        dev_assign = request.POST.get('dev_assign', '')
                        dev_hours = request.POST.get('dev_hours', '')
                        dev_int_deploy = request.POST.get('dev_int_deploy', '')
                        dev_uat_deploy = request.POST.get('dev_uat_deploy', '')
                        rvw_assign = request.POST.get('rvw_assign', '')
                        bug_ana_hours = request.POST.get('bug_ana_hours', '')
                        bug_dev_hours = request.POST.get('bug_dev_hours', '')
                        bug_td_hours = request.POST.get('bug_td_hours', '')
                        bug_test_hours = request.POST.get('bug_test_hours', '')
                        con_ques_hours = request.POST.get('con_ques_hours', '')
                        con_hours = request.POST.get('con_hours', '')
                        con_test_hours = request.POST.get('con_test_hours', '')
                        con_td_hours = request.POST.get('con_td_hours', '')
                        dev_ana_hours = request.POST.get('dev_ana_hours', '')
                        dev_dev_hours = request.POST.get('dev_dev_hours', '')
                        dev_test_hours = request.POST.get('dev_test_hours', '')
                        dev_td_hours = request.POST.get('dev_td_hours', '')
                        dev_rvw_assign = request.POST.get('dev_rvw_assign', '')
                        dev_rvw_hours = request.POST.get('dev_rvw_hours', '')
                        condev_ana_hours = request.POST.get('condev_ana_hours', '')
                        condev_dev_hours = request.POST.get('condev_dev_hours', '')
                        condev_ques_hours = request.POST.get('condev_ques_hours', '')
                        condev_con_hours = request.POST.get('condev_con_hours', '')
                        condev_test_hours = request.POST.get('condev_test_hours', '')
                        condev_td_hours = request.POST.get('condev_td_hours', '')
                        condev_rvw_assign = request.POST.get('condev_rvw_assign', '')
                        condev_rvw_hours = request.POST.get('condev_rvw_hours', '')
                        # test inputs
                        test_assign = request.POST.get('test_assign', '')
                        test_design_hours = request.POST.get('test_design_hours', '')
                        int_test_hours = request.POST.get('int_test_hours', '')
                        ipt_test_hours = request.POST.get('ipt_test_hours', '')
                        test_auto_hours = request.POST.get('test_auto_hours', '')
                        test_exec_hours = request.POST.get('test_exec_hours', '')
                        test_reg_hours = request.POST.get('test_reg_hours', '')
                        test_demo_hours = request.POST.get('test_demo_hours', '')
                        # analysis inputs
                        ana_assign = request.POST.get('ana_assign', '')
                        ana_hours = request.POST.get('ana_hours', '')
                        ana_due_dt = request.POST.get('ana_due_dt', '')
                        ana_int_rvw = request.POST.get('ana_int_rvw', '')
                        ana_td_hours = request.POST.get('ana_td_hours', '')
                        ana_fd_hours = request.POST.get('ana_fd_hours', '')
                        try:
                            dev_task_created = False
                            test_task_created = False
                            ana_task_created = False
                            # create development sub-tasks
                            if dev_assign != '':
                                if team == 'PLAT' and dev_hours != '':
                                    dev_task_created = True
                                    for dev_task in dev_tasks:
                                        if dev_task.hours[-1:] == '%':
                                            hours = int((int(dev_hours) * int(dev_task.hours[:-1])) / 100)
                                        else:
                                            hours = int(dev_task.hours[:-1])
                                        strhours = str(hours) + 'h'
                                        if dev_task.summary == 'Code Review':
                                            if rvw_assign == '':
                                                continue
                                            assignee = rvw_assign
                                        else:
                                            assignee = dev_assign
                                        task_dict = {
                                            'project': {'key': jiraapp.AppName},
                                            'parent': {'key': final_story_number},
                                            'issuetype': {'name': dev_task.type},
                                            'customfield_12200': story.fields.customfield_12200.id,
                                            'summary': dev_task.summary,
                                            'description': dev_task.description,
                                            'customfield_14313': {'id': dev_task.jteam},
                                            'customfield_14612': {'id': dev_task.application},
                                            'assignee': {'name': assignee},
                                            'timetracking': {'originalEstimate': strhours},
                                        }
                                        jira.create_issue(fields=task_dict)
                                    if dev_int_deploy != '':
                                        issue_dict = {
                                            'customfield_14624': dev_int_deploy,
                                        }
                                        story.update(fields=issue_dict)
                                    if dev_uat_deploy != '':
                                        issue_dict = {
                                            'customfield_14625': dev_uat_deploy,
                                        }
                                        if story.fields.customfield_14627.value == 'Yes':
                                            story.update(fields=issue_dict)
                                elif team == 'BWB' and story_type == 'BugFix':
                                    if bug_dev_hours != '':
                                        dev_task_created = True
                                        for dev_task in dev_tasks:
                                            if dev_task.summary == 'Analyze Root Cause':
                                                hours = bug_ana_hours
                                            elif dev_task.summary == 'Fix Defect':
                                                hours = bug_dev_hours
                                            elif dev_task.summary == 'Unit Testing':
                                                hours = bug_test_hours
                                            elif dev_task.summary == 'Technical Documentation':
                                                hours = bug_td_hours
                                            strhours = str(hours) + 'h'
                                            if strhours != 'h':
                                                task_dict = {
                                                    'project': {'key': jiraapp.AppName},
                                                    'parent': {'key': final_story_number},
                                                    'issuetype': {'name': dev_task.type},
                                                    'customfield_12200': story.fields.customfield_12200.id,
                                                    'summary': dev_task.summary,
                                                    'description': dev_task.description,
                                                    'customfield_14313': {'id': dev_task.jteam},
                                                    'customfield_14612': {'id': dev_task.application},
                                                    'assignee': {'name': dev_assign},
                                                    'timetracking': {'originalEstimate': strhours},
                                                }
                                                jira.create_issue(fields=task_dict)
                                elif team == 'BWB' and story_type == 'Configuration':
                                    for dev_task in dev_tasks:
                                        if dev_task.summary == 'Questionnaire Changes':
                                            hours = con_ques_hours
                                        elif dev_task.summary == 'Multilingual, UDP, Price changes':
                                            hours = con_hours
                                        elif dev_task.summary == 'Unit Testing':
                                            hours = con_test_hours
                                        elif dev_task.summary == 'Technical Documentation':
                                            hours = con_td_hours
                                        strhours = str(hours) + 'h'
                                        if strhours != 'h':
                                            task_dict = {
                                                'project': {'key': jiraapp.AppName},
                                                'parent': {'key': final_story_number},
                                                'issuetype': {'name': dev_task.type},
                                                'customfield_12200': story.fields.customfield_12200.id,
                                                'summary': dev_task.summary,
                                                'description': dev_task.description,
                                                'customfield_14313': {'id': dev_task.jteam},
                                                'customfield_14612': {'id': dev_task.application},
                                                'assignee': {'name': dev_assign},
                                                'timetracking': {'originalEstimate': strhours},
                                            }
                                            jira.create_issue(fields=task_dict)
                                            dev_task_created = True
                                elif team == 'BWB' and story_type == 'Development':
                                    for dev_task in dev_tasks:
                                        assignee = ''
                                        if dev_task.summary == 'Analysis':
                                            hours = dev_ana_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Code Implementation':
                                            hours = dev_dev_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Check in to GIT':
                                            hours = int(dev_task.hours[:-1])
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Code Review':
                                            hours = dev_rvw_hours
                                            if dev_rvw_assign != '':
                                                assignee = dev_rvw_assign
                                        elif dev_task.summary == 'Unit Testing':
                                            hours = dev_test_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Technical Documentation':
                                            hours = dev_td_hours
                                            assignee = dev_assign
                                        strhours = str(hours) + 'h'
                                        if strhours != 'h' and assignee != '':
                                            task_dict = {
                                                'project': {'key': jiraapp.AppName},
                                                'parent': {'key': final_story_number},
                                                'issuetype': {'name': dev_task.type},
                                                'customfield_12200': story.fields.customfield_12200.id,
                                                'summary': dev_task.summary,
                                                'description': dev_task.description,
                                                'customfield_14313': {'id': dev_task.jteam},
                                                'customfield_14612': {'id': dev_task.application},
                                                'assignee': {'name': assignee},
                                                'timetracking': {'originalEstimate': strhours},
                                            }
                                            jira.create_issue(fields=task_dict)
                                            dev_task_created = True
                                elif team == 'BWB' and story_type == 'Implementation_Configuration':
                                    for dev_task in dev_tasks:
                                        assignee = ''
                                        if dev_task.summary == 'Questionnaire Changes':
                                            hours = condev_ques_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Multilingual, UDP, Price changes':
                                            hours = condev_con_hours
                                            assignee = dev_assign
                                        if dev_task.summary == 'Analysis':
                                            hours = condev_ana_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Code Implementation':
                                            hours = condev_dev_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Check in to GIT':
                                            hours = int(dev_task.hours[:-1])
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Code Review':
                                            hours = condev_rvw_hours
                                            if condev_rvw_assign != '':
                                                assignee = condev_rvw_assign
                                        elif dev_task.summary == 'Unit Testing':
                                            hours = condev_test_hours
                                            assignee = dev_assign
                                        elif dev_task.summary == 'Technical Documentation':
                                            hours = condev_td_hours
                                            assignee = dev_assign
                                        strhours = str(hours) + 'h'
                                        if strhours != 'h' and assignee != '':
                                            task_dict = {
                                                'project': {'key': jiraapp.AppName},
                                                'parent': {'key': final_story_number},
                                                'issuetype': {'name': dev_task.type},
                                                'customfield_12200': story.fields.customfield_12200.id,
                                                'summary': dev_task.summary,
                                                'description': dev_task.description,
                                                'customfield_14313': {'id': dev_task.jteam},
                                                'customfield_14612': {'id': dev_task.application},
                                                'assignee': {'name': assignee},
                                                'timetracking': {'originalEstimate': strhours},
                                            }
                                            jira.create_issue(fields=task_dict)
                                            dev_task_created = True
                            # create test sub-tasks
                            if test_assign != '':
                                if team == 'PLAT':
                                    test_task_created = True
                                    for test_task in test_tasks:
                                        if test_task.summary == 'Test Design':
                                            if test_design_hours != '':
                                                hours = int(test_design_hours)
                                            else:
                                                hours = int(test_task.hours[:-1])
                                            assignee = test_assign
                                        elif test_task.summary == 'Test on INT':
                                            if int_test_hours == '':
                                                continue
                                            else:
                                                hours = int(int_test_hours)
                                            assignee = test_assign
                                        elif test_task.summary == 'Test on IPT':
                                            if ipt_test_hours == '':
                                                continue
                                            else:
                                                hours = int(ipt_test_hours)
                                            assignee = test_assign
                                        elif test_task.summary == 'Automation':
                                            if test_assign == '':
                                                continue
                                            if test_auto_hours != '':
                                                hours = int(test_auto_hours)
                                            else:
                                                hours = int(test_task.hours[:-1])
                                            assignee = test_assign
                                        elif test_task.summary == 'Demo Preparations':
                                            if story.fields.customfield_14627.value != 'Yes':
                                                continue
                                            hours = int(test_task.hours[:-1])
                                            assignee = test_assign
                                        else:
                                            hours = int(test_task.hours[:-1])
                                            assignee = test_assign
                                        strhours = str(hours) + 'h'
                                        task_dict = {
                                            'project': {'key': jiraapp.AppName},
                                            'parent': {'key': final_story_number},
                                            'issuetype': {'name': test_task.type},
                                            'customfield_12200': story.fields.customfield_12200.id,
                                            'summary': test_task.summary,
                                            'description': test_task.description,
                                            'customfield_14313': {'id': test_task.jteam},
                                            'customfield_14612': {'id': test_task.application},
                                            'assignee': {'name': assignee},
                                            'timetracking': {'originalEstimate': strhours},
                                        }
                                        jira.create_issue(fields=task_dict)
                                elif team == 'BWB':
                                    for test_task in test_tasks:
                                        if test_task.summary == 'Test Case Preparation':
                                            hours = test_design_hours
                                        elif test_task.summary == 'Test Case Execution':
                                            hours = test_exec_hours
                                        elif test_task.summary == 'Regression Test Execution':
                                            hours = test_reg_hours
                                        elif test_task.summary == 'Demo to Support & Business':
                                            hours = test_demo_hours
                                        strhours = str(hours) + 'h'
                                        if strhours != 'h':
                                            task_dict = {
                                                'project': {'key': jiraapp.AppName},
                                                'parent': {'key': final_story_number},
                                                'issuetype': {'name': test_task.type},
                                                'customfield_12200': story.fields.customfield_12200.id,
                                                'summary': test_task.summary,
                                                'description': test_task.description,
                                                'customfield_14313': {'id': test_task.jteam},
                                                'customfield_14612': {'id': test_task.application},
                                                'assignee': {'name': test_assign},
                                                'timetracking': {'originalEstimate': strhours},
                                            }
                                            jira.create_issue(fields=task_dict)
                                            test_task_created = True
                            # create analysis sub-tasks
                            if ana_assign != '' and ana_hours != '':
                                ana_task_created = True
                                for ana_task in ana_tasks:
                                    if ana_task.summary == 'Analysis':
                                        hours = int(ana_hours)
                                        assignee = ana_assign
                                    elif ana_task.summary == 'Internal Review':
                                        if ana_int_rvw == 'No':
                                            continue
                                        else:
                                            hours = int(ana_task.hours[:-1])
                                        assignee = ana_assign
                                    elif ana_task.summary == 'Functional Documentation':
                                        if team == 'PLAT':
                                            hours = int(ana_task.hours[:-1])
                                        elif team == 'BWB':
                                            hours = ana_fd_hours
                                        assignee = ana_assign
                                    elif ana_task.summary == 'Technical Documentation':
                                        if team == 'BWB':
                                            hours = ana_td_hours
                                        assignee = ana_assign
                                    else:
                                        hours = int(ana_task.hours[:-1])
                                        assignee = ana_assign
                                    strhours = str(hours) + 'h'
                                    if strhours != 'h':
                                        task_dict = {
                                            'project': {'key': jiraapp.AppName},
                                            'parent': {'key': final_story_number},
                                            'issuetype': {'name': ana_task.type},
                                            'customfield_12200': story.fields.customfield_12200.id,
                                            'summary': ana_task.summary,
                                            'description': ana_task.description,
                                            'customfield_14313': {'id': ana_task.jteam},
                                            'customfield_14612': {'id': ana_task.application},
                                            'assignee': {'name': assignee},
                                            'timetracking': {'originalEstimate': strhours},
                                        }
                                        jira.create_issue(fields=task_dict)
                                if ana_due_dt != '':
                                    issue_dict = {
                                        'duedate': ana_due_dt,
                                    }
                                    story.update(fields=issue_dict)
                            # Assign story
                            if team == 'PLAT':
                                if (story_type == "AnalysisDevelopment" or story_type == "Analysis") and (ana_assign != '' and ana_hours != ''):
                                    story.assignee = ana_assign
                                    story_dict = {
                                        'assignee': {'name': ana_assign},
                                    }
                                    story.update(fields=story_dict)
                                elif story_type == "Development" and (dev_assign != '' and dev_hours != ''):
                                    story.assignee = dev_assign
                                    story_dict = {
                                        'assignee': {'name': dev_assign},
                                    }
                                    story.update(fields=story_dict)
                                elif story_type == "Testing" and test_assign != '':
                                    story.assignee = test_assign
                                    story_dict = {
                                        'assignee': {'name': test_assign},
                                    }
                                    story.update(fields=story_dict)
                            elif team == 'BWB':
                                if (story_type == "Analysis") and (ana_assign != '' and ana_hours != ''):
                                    story.assignee = ana_assign
                                    story_dict = {
                                        'assignee': {'name': ana_assign},
                                    }
                                    story.update(fields=story_dict)
                                elif (story_type == "BugFix") and (dev_assign != '' and bug_dev_hours != ''):
                                    story.assignee = dev_assign
                                    story_dict = {
                                        'assignee': {'name': dev_assign},
                                    }
                                    story.update(fields=story_dict)
                            if dev_task_created:
                                messages.success(request, 'Development tasks are created successfully.')
                            if test_task_created:
                                messages.success(request, 'Testing tasks are created successfully.')
                            if ana_task_created:
                                messages.success(request, 'Analysis tasks are created successfully.')
                            if dev_task_created or test_task_created or ana_task_created:
                                story.fields.labels.append(u'sub_tasks_auto_created')
                                story.update(fields={"labels": story.fields.labels})
                            else:
                                messages.warning(request, 'Nothing to create!')
                        except JIRAError as e:
                            messages.error(request, e.text, 'danger')
                        return render(request, 'jira_sub_tasks/home.html', {
                            'jira': jira,
                            'story_number': story_number,
                            'story': story,
                            'userDispName': userDispName,
                            'story_type': story_type,
                            'dev_tasks': dev_tasks,
                            'test_tasks': test_tasks,
                            'dev_display': dev_display,
                            'test_display': test_display,
                            'ana_display': ana_display,
                            'ana_tasks': ana_tasks,
                            'devusers': devusers,
                            'testusers': testusers,
                            'anausers': anausers,
                            'sprintName': sprintName,
                            'status': status,
                            'labels': labels,
                        })

                    return render(request, 'jira_sub_tasks/home.html', {
                        'jira': jira,
                        'story_number': story_number,
                        'story': story,
                        'userDispName': userDispName,
                        'story_type': story_type,
                        'dev_tasks': dev_tasks,
                        'test_tasks': test_tasks,
                        'dev_display': dev_display,
                        'test_display': test_display,
                        'ana_display': ana_display,
                        'ana_tasks': ana_tasks,
                        'devusers': devusers,
                        'testusers': testusers,
                        'anausers': anausers,
                        'sprintName': sprintName,
                        'status': status,
                        'labels': labels,
                    })
                except JIRAError as e:
                    messages.error(request, e.text, 'danger')
                    return render(request, 'jira_sub_tasks/home.html', {
                        'jira': jira,
                        'story_number': story_number,
                        'userDispName': userDispName,
                    })
            else:
                return render(request, 'jira_sub_tasks/home.html', {
                    'jira': jira,
                    'userDispName': userDispName,
                })
        else:
            return render(request, 'jira_sub_tasks/home.html', {'jira': jira, 'userDispName': userDispName})
    except KeyError:
        return redirect('login')


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            successMessage = 'You\'re now successfully logged in as ' + JIRAUsers.objects.filter(
                key=form.cleaned_data.get('username')).first().displayName + '!'
            messages.success(request, successMessage)
            request.session['username'] = form.cleaned_data.get('username')
            request.session['password'] = form.cleaned_data.get('password')
            request.session['team'] = form.cleaned_data.get('select_team')
            return redirect('jira_sub_tasks_home')
    else:
        try:
            username = request.session['username']
            return redirect('jira_sub_tasks_home')
        except KeyError:
            form = UserLoginForm()
    return render(request, 'jira_sub_tasks/login.html', {'form': form})


def logout(request):
    try:
        del request.session['username']
        del request.session['password']
        messages.info(request, 'You\'re now logged out!')
    except KeyError:
        messages.warning(request, 'Please login first!')
    return redirect('login')


def privacy(request):
    return render(request, 'jira_sub_tasks/privacy.html')


def backlog(request):
    backlogs = Backlog.objects.all()
    return render(request, 'jira_sub_tasks/backlog.html', {'backlogs': backlogs})


def landing(request):
    return render(request, 'jira_sub_tasks/landing.html')
