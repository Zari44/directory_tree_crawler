import time
import threading

list = []

def append_list():
    if not list:
        next_element = 0
    else:
        next_element = list[-1]+1
    list.append(next_element)
    return next_element

if __name__ == '__main__':
    list = []
    start_time = time.time()
    max_time_s = 10
    thread1 = threading.Thread(target=append_list)
    thread1.start()
    while(time.time() - start_time < max_time_s):
        time.sleep(1)
        print(append_list())
    print(list)





