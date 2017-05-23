from tentacle.scheduler import register, register_list, crawl
import boto3
from moto import mock_s3
from core.utils import s3Utils
import pytest


def mocked_s3():
    '''
    don't put this as a fixutre so it will be called within
    the s3 mock decorators on the associated tests
    '''
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='dbmi-repo-registry')
    conn.create_bucket(Bucket='tc-systems')

    return s3Utils(outfile_bucket='tc-systems', sys_bucket='dbmi-repo-registry')


@mock_s3
def test_register():
    register("test_file", "http://blah.blah", s3utils=mocked_s3())


@mock_s3
def test_register_duplicate():
    register("test_file", "http://blah.blah", s3utils=mocked_s3())
    with pytest.raises(Exception) as exc_info:
        register("test_file", "http://blah.blah", s3utils=mocked_s3())

    assert str(exc_info.value).startswith("Already registered")


@mock_s3
def test_register_then_update():

    s3 = mocked_s3()
    register("test_file", "http://blah.blah", s3utils=s3)
    register("test_file", "http://blah.updated", s3utils=s3,
             update=True)

    assert s3.read_s3('test_file') == b'http://blah.updated'


@mock_s3
def test_get_registered():

    s3utils = mocked_s3()
    register("test_file", "http://blah.test", s3utils=s3utils)
    register("test_file2", "http://blah.test2", s3utils=s3utils)
    register("test_file3", "http://blah.test3", s3utils=s3utils)
    regs = register_list(s3utils=s3utils)
    assert len(regs) == 3
    assert regs['test_file3'] == b'http://blah.test3'
    assert regs['test_file2'] == b'http://blah.test2'
    assert regs['test_file'] == b'http://blah.test'


def print_em(item):
    assert len(item) == 2


@mock_s3
def test_crawl():

    s3utils = mocked_s3()
    register("test_file", "http://blah.test", s3utils=s3utils)
    register("test_file2", "http://blah.test2", s3utils=s3utils)
    register("test_file3", "http://blah.test3", s3utils=s3utils)
    crawl(s3utils, print_em)
