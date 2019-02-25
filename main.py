import os
import queue
import threading
import logging
import time


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


task_queue = TaskQueue()

# dirs = queue.Queue()
# tasks = queue.Queue()

lock = threading.Lock()

no_files = 0


class CrawlingThread(threading.Thread):

    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.thread_name = thread_name

    def run(self):
        logging.warning('Starting ' + self.thread_name)
        crawl_tq(task_queue)
        logging.warning('Stopping ' + self.thread_name)


def crawl_tq(task_queue):
    global no_files

    while task_queue.are_running_tasks():
        if task_queue.available_tasks():
            root_dir = task_queue.get()
            try:
                print(root_dir)
                files = os.listdir(root_dir)
            except:
                logging.warning("Exception!")
            for file in files:
                file_path_abs = os.path.join(root_dir, file)

                if os.path.isdir(file_path_abs) and os.access(file_path_abs, os.R_OK):
                    task_queue.put(file_path_abs)
                elif os.path.islink(file_path_abs):
                    # print(file)
                    pass
                else:
                    # print(file)
                    pass

                with lock:
                    no_files += 1
            task_queue.task_finished()


if __name__ == "__main__":
    root_path = '/home.cezary/szeliga'
    # root_path = '/home.cezary/kozlowski'
    # root_path = '/home.cezary/welnicki'
    # root_path = "/home.cezary/groupfiles/shared/sales"

    n = 5

    task_queue.put(root_path)

    threads = []
    for i in range(1, n+1):
        thread = CrawlingThread("thread"+str(i))
        threads.append(thread)

    start = time.time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logging.warning("Time took: %0.2f", time.time()-start)
    logging.warning("Visited %s files ", no_files)

    logging.warning("Exiting Main Thread")
