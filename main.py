import os
import queue
import threading
import logging
import time
from pathlib import Path


logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'
)


class TaskQueue:

    def __init__(self):
        self._tasks = queue.Queue()
        self._running_tasks = queue.Queue()

    def are_running_tasks(self):
        return not self._running_tasks.empty()

    def no_available_tasks(self):
        return self._tasks.empty()

    def available_tasks(self):
        return self._tasks.qsize()

    def put(self, directory_path):
        self._tasks.put(directory_path)
        self._running_tasks.put(None)

    def get(self):
        return self._tasks.get()

    def task_finished(self):
        self._running_tasks.get()


class CrawlingThread(threading.Thread):

    def __init__(self, _id):
        threading.Thread.__init__(self)
        self._id = _id

    def run(self):
        logging.warning('Starting Thread ', self._id)
        ThreadedCrawler.__crawl()
        logging.warning('Stopping Thread ', self._id)


class ThreadedCrawler:

    def __init__(self, root_dir, no_threads):
        self._root_dir = root_dir
        self._no_threads = no_threads
        self._task_queue = TaskQueue()
        self._task_queue.put(root_dir)
        self._threads = []
        self.__create_threads(no_threads)
        self._lock = threading.Lock()
        self._no_files_visited = 0

    def __create_threads(self, no_threads):
        self._threads = [threading.Thread(target=self.__crawl) for _ in range(no_threads)]# CrawlingThread(i)

    def start_crawling(self):

        logging.warning("Started crawling files starting from root directory '%s' utilising %s threads",
                        self._root_dir, self._no_threads)

        for thread in self._threads:
            logging.warning("Starting new thread")
            thread.start()

        for thread in self._threads:
            thread.join()

    def __crawl(self):
        while self._task_queue .are_running_tasks():
            if self._task_queue .available_tasks():
                root_dir = self._task_queue .get()
                files = []
                try:
                    files = os.listdir(root_dir)
                    print(root_dir)
                except OSError as e:
                    print(str(e))
                except UnicodeError as e:
                    print(str(e))
                for file in files:
                    file_path_abs = os.path.join(root_dir, file)

                    if os.path.isdir(file_path_abs):
                        self._task_queue .put(file_path_abs)
                    elif os.path.islink(file_path_abs):
                        first_target = os.readlink(file_path_abs)
                        ultimate_target = ""
                        if os.path.islink(first_target):
                            ultimate_target = "->" + Path(file_path_abs).resolve()
                        print(file, '->', first_target, ultimate_target)
                    else:
                        print(file)

                    with self._lock:
                        self._no_files_visited += 1
                self._task_queue.task_finished()

    def get_no_files_visited(self):
        return self._no_files_visited


if __name__ == "__main__":

    root_path = '/home/'
    n = 5

    crawler = ThreadedCrawler(root_path, n)

    start = time.time()
    crawler.start_crawling()
    logging.warning("Time took: %0.2f", time.time()-start)

    logging.warning("%s files were accessed from '%s'", crawler.get_no_files_visited(), root_path)
