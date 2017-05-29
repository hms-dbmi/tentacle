import yaml


class DBMIProject(yaml.YAMLObject):
    yaml_tag = "!DBMIProject"

    @classmethod
    def from_yml(cls, path):
        '''
        of course nobody would ever pass me anything
        malicious or not DBMIProject
        '''
        return yaml.load(open(path))

    def __init__(self, project, description, lab,
                 authors, languages, tags='',
                 needs=None, packages=None, url='',
                 stars=0, watchers=0, forks=0):
        self.project = project
        self.description = description
        self.lab = lab
        self.authors = authors
        self.lanugages = languages
        self.tags = tags
        self.needs = needs
        self.packages = packages
        self.url = url
        self.stars = stars
        self.watchers = watchers
        self.forks = forks

    def __str__(self):
        return yaml.dump(self)

    def to_markdown(self):
        '''
        spit out a markdown representation of
        our object
        '''
        # TODO: format lists to not have lists...
        md = '''
             |             |                 |
             |-------------|-----------------|
             | Name        | {project}       |
             | Author      | {authors}       |
             | Lab         | {lab}           |
             | URL         | {url}           | | Description | {description}   |
             | Tags        | {tags}          |
             | Packages    | {packages}      |
             '''
        return md.format(**self.__dict__)
