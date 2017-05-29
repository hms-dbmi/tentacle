import os
import requests
# from requests.exceptions import RequestException
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


class GithubCrawler(object):
    """
        Crawl github organizations and gather various info for exporting
    """

    def __init__(self, organization, model=None):
        """
        organization: String containing github org. to crawl
        model: Instance of a tentacle model class for exporting purposes
        """
        if organization is None:
            raise RuntimeError("A github organization is required.")

        self.organization = organization
        self.base_api_url = 'https://api.github.com/'
        self.base_org_url = "%sorgs/%s/" % (self.base_api_url, organization)
        self.headers = {
            'Authorization': 'token %s' % os.getenv("DBMI_TOKEN")
        }
        self.model = model

    def __str__(self):
        return "<Crawler>: {}".format(
            self.organization
        )

    def _request(self, urltail):
        url = urljoin(self.base_api_url, urltail)
        response = requests.get(
            url,
            headers=self.headers
        )
        return response.content

    def get_org_info(self):
        return self._request('orgs/%s' % self.organization)

    def get_repos(self):
        return self._request('orgs/%s/repos' % self.organization)

    def get_contributors(self, repo_full_name):
        return self._request('repos/%s/collaborators' % repo_full_name)
