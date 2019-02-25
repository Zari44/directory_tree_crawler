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
        self.dirs = queue.Queue()
        self.tasks = queue.Queue()

    def no_running_tasks(self):
        return self.tasks.empty()

    def running_tasks(self):
        return self.tasks.qsize()

    def no_directories(self):
        return self.dirs.empty()

    def put(self, directory_path):
        self.dirs.put(directory_path)
        self.tasks.put(None)

    def get_directory(self):
        return self.dirs.get()

    def task_finished(self):
        self.tasks.get()


task_queue = TaskQueue()

dirs = queue.Queue()
tasks = queue.Queue()

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


def crawl(dirs_):
    global no_files

    while not tasks.empty():
        if dirs_.empty():
            pass
        else:
            root_dir = dirs_.get()
            try:
                print(root_dir)
                files = os.listdir(root_dir)
            except:
                logging.warning("Exception!")
            for file in files:
                file_path_abs = os.path.join(root_dir, file)

                if os.path.isdir(file_path_abs) and os.access(file_path_abs, os.R_OK):
                    dirs_.put(file_path_abs)
                    tasks.put(None)
                elif os.path.islink(file_path_abs):
                    # print(file)
                    pass
                else:
                    # print(file)
                    pass
                with lock.acquire():
                    no_files += 1
            tasks.get()


def crawl_tq(task_queue):
    global no_files

    while task_queue.running_tasks():
        if task_queue.no_directories():
            pass
        else:
            root_dir = task_queue.get_directory()
            try:
                print(root_dir)
                files = os.listdir(root_dir)
            except:
                logging.warning("Exception!")
            for file in files:
                file_path_abs = os.path.join(root_dir, file)

                if os.path.isdir(file_path_abs) and os.access(file_path_abs, os.R_OK):
                    task_queue.put(file_path_abs)
                    tasks.put(None)
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
    root_path = '/home'
      
    n = 5

    task_queue.put(root_path)

    # dirs.put(root_path)
    # tasks.put(None)
    threads = []
    for i in range(1,n+1):
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
