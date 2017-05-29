from tentacle.crawlers.github import GithubCrawler
import json
from tentacle.model.dbmi import DBMIProject


def test_get_org_info():
    gh = GithubCrawler('4dn-dcic')
    resp = gh.get_org_info()
    resp_json = json.loads(resp)
    assert resp_json['login'] == '4dn-dcic'


def test_get_repos():
    gh = GithubCrawler('4dn-dcic')
    resp = gh.get_repos()
    resp_json = json.loads(resp)
    assert len(resp_json) > 2

    for repo in resp_json:
        url = repo.get('homepage')
        if not url or url == 'null':
            url = repo.get('html_url')

        # TODO get authors from contributors url
        authors = ['--', ]
        contribs = json.loads(gh.get_contributors(repo['full_name']))

        if isinstance(contribs, (list, tuple)):
            # TODO: get authors github url as well, so we can build links
            authors = [contrib['login'] for contrib in contribs]
        else:
            print("no authors found from github")

        proj = DBMIProject(project=repo['name'],
                           description=repo.get('description'),
                           languages=repo.get('language'),
                           lab=gh.organization,
                           authors=authors,
                           url=url,
                           stars=repo.get('stargazers_count'),
                           watchers=repo.get('watchers_count'),
                           forks=repo.get('forks'),
                           )
        print(proj)
