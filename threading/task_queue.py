from Queue import Queue
from threading import Thread
import time

task_queue = Queue()
completion_queue = Queue()

def my_method(in_queue, out_queue):
    while True:
        task = in_queue.get()
        time.sleep((task + 2) * 3)
        in_queue.task_done()

        # Send completion message
        out_queue.put(task)

num_queue_threads = 2
queue_threads = [None] * num_queue_threads

for i in range(num_queue_threads):
    queue_threads[i] = Thread(target=my_method, args=(task_queue, completion_queue))
    queue_threads[i].setDaemon(True)
    queue_threads[i].start()

for task in range(3):
    task_queue.put(task)

for _ in range(3):
    completion_queue.get()
    completion_queue.task_done()
    print("One task done!")

print("All done!")