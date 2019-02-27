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


def crawl(dirs):
    while dirs.qsize():
        files = []
        symlinks = []
        directories = []
        dir_path = dirs.get()
        try:
            for entry in os.scandir(dir_path):
                if entry.is_symlink():
                    symlinks.append(entry)
                elif entry.is_dir():
                    dirs.put(entry.path)
                    directories.append(entry)
                else:
                    files.append(entry)
        except OSError as e:
            print("Error occured: %s" % str(e))
        finally:
            yield {dir_path: [directories, files, symlinks]}


def print_dict(dirs_dict):
    for catalog in dirs_dict:
        print(catalog)
        for directory in dirs_dict[catalog][0]:
            print("\t", directory.name)
        for file in dirs_dict[catalog][1]:
            print("\t", file.name)
        for symlink in dirs_dict[catalog][2]:
            print("\t", symlink.name, "->", os.readlink(symlink.path))


if __name__ == "__main__":

    # root_path = '/home/zarudzki_biz9ld/java_workspace'
    # root_path = '/home/zarudzki_biz9ld/Downloads/Postman/app/resources/app/node_modules/@postman/app-plugins-host/node_modules/@postman/app-logger/node_modules/readable-stream/lib/internal/'
    root_path = './tests'
    n = 5

    print("Starting the scanner in root directory: '%s'" % (root_path))

    start = time.time()

    dirs = queue.Queue()
    dirs.put(root_path)
    for dir in crawl(dirs):
        print_dict(dir)

    print("Time took: %0.2f" % (time.time()-start))
    print("%s files were accessed from '%s'" % (0, root_path))
