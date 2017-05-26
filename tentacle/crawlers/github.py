import os
import requests
from requests.exceptions import RequestException
from urlparse import urljoin


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

        self.base_api_url = "https://api.github.com"
        self.headers = {
            'Authorization': 'token %s' % os.getenv("DBMI_TOKEN")
        }
        self.organization = organization
        self.model = model

    def __str__(self):
        return "<Crawler>: {}".format(
            self.organization
        )

    def get_org_info(self):
        try:
            response = requests.get(
                urljoin(
                    self.base_api_url,
                    "/orgs/{}".format(self.organization)
                ),
                headers=self.headers
            )
        except RequestException as e:
            print e
        else:
            print response.content
