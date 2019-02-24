import os
import queue
import threading
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'
)

dirs = queue.Queue()

class crawlingThread (threading.Thread):


   def __init__(self, thread_name):
      threading.Thread.__init__(self)
      self.thread_name = thread_name


   def run(self):
      logging.warning('Starting ' + self.thread_name)
      crawl_utils(dirs)
      logging.warning('Stopping ' + self.thread_name)


def crawl(root_dir, n = 1):
    dirs.put(root_dir)
    threads_pool = []
    for i in range(1,n+1):
        thread = crawlingThread("thread"+str(i))
        thread.start()
        threads_pool.append(thread)


def crawl_utils(dirs):
    while not dirs.empty():
        root_dir = dirs.get()
        print(root_dir)
        files = os.listdir(root_dir)
        for file in files:
            file_path_abs = os.path.join(root_dir, file)

            if os.path.isdir(file_path_abs) and \
                    os.access(file_path_abs, os.R_OK) and \
                    not os.path.islink(file_path_abs):
                dirs.put(file_path_abs)
            else:
                print(file)


if __name__ == "__main__":
    root_dir = '/home/mzarudzki/qt_workspace'
    crawl(root_dir, 10)
    logging.warning("Exiting Main Thread")
