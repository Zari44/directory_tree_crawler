import os


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


if __name__ == "__main__":
    rootDir = '/home/mzarudzki/crawler_test'
    lvl = 0
    for dirName, subdirList, fileList in os.walk(rootDir,
                                                 topdown=True,
                                                 followlinks=False):
        print_dir_tree(dirName, fileList, lvl)
        lvl += 1


