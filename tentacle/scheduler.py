'''
KISS scheduler, simply store list of registered urls on s3 file
'''
from core.utils import s3Utils
from botocore.exceptions import ClientError
import logging
from multiprocessing import cpu_count  # pylint: disable=no-name-in-module
from multiprocessing import Pool  # pylint: disable=no-name-in-module


log = logging.getLogger(__name__)

s3 = s3Utils(outfile_bucket='tc-systems', sys_bucket='dbmi-repo-registry')


def register(name, url, s3utils, update=False):
    '''
    register just by writting a new file to s3 with key=name and data=url
    '''
    try:
        exists = s3utils.read_s3(name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            exists = False

    if exists and update is False:
        raise Exception("Already registered, use update option")

    return s3utils.s3_put(url, name)


def register_list(s3utils):
    resp = s3utils.s3_read_dir('')
    content = resp.get('Contents', [])
    urls = {}
    # TODO, add in ghkeys as an attribute to the list maybe?
    for c in content:
        urls[c['Key']] = s3utils.read_s3(c['Key'])
    return urls


def crawl(s3utils, crawler):
    '''
    crawler and report should be functions

    '''
    urls = register_list(s3utils)
    tasks = ParallelTask(crawler)
    for task in tasks.run(urls.items()):
        pass


class ParallelTask(object):
    def __init__(self, task_func, num_cpu=None, no_parallel=False):
        """
        Args:
          - task_func (callable): Task to run on each work item. Must be a
              global function, or instance of a global class, due to
              multiprocessing's limitations.
          - no_parallel (bool): If true, run everything in the main thread.
        """
        self.task_func = task_func
        self.no_parallel = no_parallel
        self.num_cpu = num_cpu or cpu_count() - 1

    def run(self, items, chunk_size=1):
        """Run task in parallel on a list of work items.

        Uses multiprocessing in order to avoid Python's GIL.
        """
        if not self.no_parallel:
            with Pool(self.num_cpu) as pool:
                for res in pool.imap(self.task_func, items, chunk_size):
                    yield res
        else:
            for res in map(self.task_func, items):
                yield res
