from issue_tracker.models import Project, Issue


def get_all_projects():
    return Project.objects.filter(is_deleted=False)


def get_issues():
    return Issue.objects.filter(is_deleted=False)

