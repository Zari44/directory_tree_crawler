import os
import queue
import logging
import threading
import time


logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'
)

no_files = 0

def crawl(dirs_queue, tasks, lock):
    global no_files
    while not tasks.empty():
        if dirs_queue.empty():
            pass
        else:
            root_dir = dirs_queue.get()
            print(root_dir)
            files = os.listdir(root_dir)
            for file in files:
                lock.acquire()
                no_files += 1
                lock.release()
                file_path_abs = os.path.join(root_dir, file)
                if os.path.isdir(file_path_abs) and os.access(file_path_abs, os.R_OK) and not os.path.islink(file_path_abs):
                    dirs_queue.put(file_path_abs)
                    tasks.put(None)
                else:
                    print(file)
            tasks.get()


class Crawler(threading.Thread):
  def __init__(self, id, dirs, tasks, queueLock):
    threading.Thread.__init__(self)
    self._dirs = dirs
    self._id = id
    self._tasks = tasks
    self._queueLock = queueLock

  def run(self):
      logging.warning("Start Thread " + str(self._id))
      crawl(self._dirs, self._tasks, self._queueLock)
      logging.warning("Stop Thread " + str(self._id))


if __name__ == "__main__":
    # root_path = '/home/mzarudzki/machine_learning_datasets'#qt_workspace'
    root_path = '/home/mzarudzki/machine_learning_datasets'  # qt_workspace'

    q_tasks = queue.Queue();
    q_dirs = queue.Queue()
    q_dirs.put(root_path)
    q_tasks.put(None)
    queueLock = threading.Lock()

    n = 4
    start_time = time.time()

    workers = []
    for i in range(n):
        worker = Crawler(i, q_dirs, q_tasks, queueLock)
        workers.append(worker)

    for worker in workers:
        worker.start()

    # q_dirs.join()

    for worker in workers:
        worker.join()

    logging.warning("time = %.2f" % (time.time()-start_time))
    logging.warning("no files seen: %d", no_files)
    logging.warning("Exiting Main Thread")