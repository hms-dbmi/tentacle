import yaml2

def parse_yml(yml_file):
    '''
    returns a python dictionary
    of the object
    '''
    return yaml2.load(open(yml_file))


# do some serializer stuff here
# how about make a model just like django..

class DBMIProject(yaml2.YAMLObject):
    yaml_tag = "!DBMIProject"
    def __init__(self, project, description, lab,
                 authors, languages, tags,
                 needs=None, packages=None):
        self.project = project
        self.description = description
        self.lab = lab
        self.authors = authors
        self.lanugages = languages
        self.tags = tags
        self.needs = needs
        self.packages = packages

    def __str__(self):
        return yaml2.dump(self)

    def to_markdown(self):
        '''
        spit out a markdown representation of
        our object
        '''
        # TODO: format lists to not have lists...
        md = '''
             |             |                 |
             |-------------|-----------------|
             | Name        | {name}          |
             | Author      | {authors}       |
             | Lab         | {lab}           |
             | URL         | {url}           |
             | Description | {description}   |
             | Tags        | {tags}          |
             | Packages    | {packages}      |
             '''
        return md.format(**self.__dict__)








