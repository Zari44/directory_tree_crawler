import os
import queue


def print_identation(n):
    i = 0
    while i < n:
        print('\t', end='')
        i += 1


def print_dir(dirName, lvl = 0):
    print_identation(lvl)
    print(dirName)


def print_filename(filename, lvl = 0):
    print_identation(lvl)
    print('\t%s' % filename)


def print_dir_tree(dirName, fileList, lvl):
    print_dir(dirName, lvl)
    for fname in fileList:
        print_filename(fname, lvl)


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
                print(file_path_abs)


if __name__ == "__main__":
    root_dir = '/home/mzarudzki/crawler_test'
    crawl(root_dir)
