'''
KISS scheduler, simply store list of registered urls on s3 file
'''
import time
from core.utils import s3Utils
from botocore.exceptions import ClientError
import logging
from concurrent.futures import ThreadPoolExecutor


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


def crawl(s3utils, crawler, threads=10):
    '''
    crawler and report should be functions

    '''
    urls = register_list(s3utils)
    tasks = ThreadedTask(crawler)
    timer = Stopwatch()
    for task in tasks.run(urls.items()):
        pass

    num_repos = len(urls.items())
    log.debug('Crawled: %d repos at %.0f repos/s', num_repos,
              num_repos / timer.elapsed)


class Stopwatch(object):
    def __init__(self):
        try:
            self.timer = time.perf_counter
        except AttributeError:
            self.timer = time.time

        self.start = self.timer()

    @property
    def elapsed(self):
        return self.timer() - self.start


class ThreadedTask(object):
    def __init__(self, task_func, threads=10, no_parallel=False):
        """
        Args:
          - task_func (callable): Task to run on each work item.
          - no_parallel (bool): If true, run everything in the main thread.
        """
        self.task_func = task_func
        self.no_parallel = no_parallel
        self.threads = threads

    def run(self, items):
        """Run task concurrently on a list of work items.
           Currently this is threaded so not parallel
        """
        if not self.no_parallel:
            with ThreadPoolExecutor(max_workers=self.threads) as pool:
                for res in pool.map(self.task_func, items):
                    yield res
        else:
            for res in map(self.task_func, items):
                yield res
