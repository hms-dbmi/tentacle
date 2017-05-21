from tentacle.model.dbmi import DBMIProject


def test_from_yml(dbmi_yml_path):
    proj = DBMIProject.from_yml(dbmi_yml_path)
    assert proj
    assert type(proj) == DBMIProject
    assert proj.project
    assert proj.description
    assert proj.lab
    assert proj.authors


def test_to_markdown():
    proj = DBMIProject('test', 'desc', 'lab',
                       ['jack', 'frost'],
                       ["python"],
                       ["testware"]
                       )

    md = proj.to_markdown()
    assert md.find('Name') < md.find(proj.project)
    assert md.find('Author') < md.find(proj.authors[0])
    assert md.find(proj.authors[0]) < md.find(proj.authors[1])
