from github import Github, GithubException
from django.conf import settings


instance = Github(login_or_token=settings.GH_TOKEN)


class GithubAPI:
    @staticmethod
    def get_contributors(owner_and_repo_name):
        contributors = []
        try:
            response = instance \
                .get_repo(owner_and_repo_name) \
                .get_contributors()
        except GithubException:
            return contributors
        else:
            for contributor in response:
                contributors.append({
                    'username': contributor.login,
                    'url': contributor.html_url,
                    'image_url': contributor.avatar_url
                })
            return contributors
