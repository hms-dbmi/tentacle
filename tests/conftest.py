import pytest
import os


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def dbmi_yml_path():
    return os.path.join(here, "..", ".dbmi.yml")


@pytest.fixture(scope='session')
def dbmi_yml(dbmi_yml_path):
    with open(dbmi_yml_path, "r") as dbmi_yml:
        return dbmi_yml.readlines()
