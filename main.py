import os
import queue
import threading


class myThread (threading.Thread):


   def __init__(self, root_dir):
      threading.Thread.__init__(self)
      self.root_dir = root_dir


   def run(self):
      print ("Starting scrawling " + self.root_dir)
      crawl(self.root_dir)
      print ("Exiting scrawling " + self.root_dir)


def crawl(root_dir):
    dirs = queue.Queue()
    dirs.put(root_dir)
    while not dirs.empty():
        root_dir = dirs.get()
        print(root_dir)
        files = os.listdir(root_dir)
        for file in files:
            file_path_abs = os.path.join(root_dir, file)
            if os.path.isdir(file_path_abs):
                dirs.put(file_path_abs)
            else:
                print(file)


if __name__ == "__main__":
    root_dir = '/home/mzarudzki/crawler_test'

    # Create new threads
    thread1 = myThread(root_dir)

    # Start new Threads
    thread1.start()
    thread1.join()
    print("Exiting Main Thread")

