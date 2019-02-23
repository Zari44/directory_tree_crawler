import os

class Crawler:

    def __init__(self, root_path):
        self.__root_path = root_path

    def listDir(self):
        return os.listdir(self.__root_path)

    def getRootPath(self):
        return self.__root_path

if __name__ == "__main__":
    crawler = Crawler('/home/mzarudzki/crawler_test')
    print(crawler.listDir())


