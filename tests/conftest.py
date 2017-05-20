import pytest
import os

here = os.path.abspath(os.path.dirname(__file__))
@pytest.fixture(scope='session')
def dbmi_yml():
    path = os.path.join(here,"..","..",".dbmi.yml")
    with open(path, "r") as dbmi_yml:
        return dmi_yml.read_all()
