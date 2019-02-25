import os
import queue
import threading
import logging
import time


logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'
)

dirs = queue.Queue()
tasks = queue.Queue()

no_files = 0

class CrawlingThread (threading.Thread):

   def __init__(self, thread_name):
      threading.Thread.__init__(self)
      self.thread_name = thread_name

   def run(self):
      logging.warning('Starting ' + self.thread_name)
      crawl(dirs)
      logging.warning('Stopping ' + self.thread_name)




def crawl(dirs):

    while not tasks.empty():
        if dirs.empty():
            pass
        else:
            root_dir = dirs.get()
            print(root_dir)
            files = os.listdir(root_dir)
            for file in files:
                file_path_abs = os.path.join(root_dir, file)

                if os.path.isdir(file_path_abs) and os.access(file_path_abs, os.R_OK):
                    dirs.put(file_path_abs)
                    tasks.put(None)
                elif os.path.islink(file_path_abs):
                    print(file)
                else:
                    print(file)
                global  no_files
                no_files += 1
            tasks.get()


if __name__ == "__main__":
    root_path = '/home/zarudzki_biz9ld/python_workspace'
    n = 1

    dirs.put(root_path)
    tasks.put(None)
    threads = []
    for i in range(1,n+1):
        thread = CrawlingThread("thread"+str(i))
        threads.append(thread)

    start = time.time()

    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()

    logging.warning("Time took: %s", time.time()-start)
    logging.warning("Visited %s files ", no_files)

    logging.warning("Exiting Main Thread")
