from github import Github, GithubException
from django.conf import settings


github = Github(login_or_token=settings.GH_TOKEN)


def get_contributors(owner, repository):
    repo_key = '{owner}/{repository}'.format(
        owner=owner,
        repository=repository,
    )

    contributors = []

    try:
        response = (
            github.get_repo(repo_key)
                  .get_contributors()
        )
    except GithubException:
        pass

    else:
        contributors = [
            {
                'username': contributor.login,
                'url': contributor.html_url,
                'image_url': contributor.avatar_url
            }
            for contributor in response
        ]

    return contributors
