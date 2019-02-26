import os
import queue
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'
)

def crawl(root_dir):
    dirs = queue.Queue()
    dirs.put(root_dir)
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
    crawl(root_dir)
    logging.warning("Exiting Main Thread")