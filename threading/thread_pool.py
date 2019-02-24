import urllib2
from multiprocessing.dummy import Pool as ThreadPool
import time

urls = [
  'http://www.python.org',
  'http://www.python.org/about/',
  'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
  'http://www.python.org/doc/',
  'http://www.python.org/download/',
  'http://www.python.org/getit/',
  'http://www.python.org/community/',
  'https://wiki.python.org/moin/',
  'http://google.com',
  'http://www.alibaba.com',
  'http://www.dropbox.com',
]

start_time = time.time()
# make the Pool of workers
pool = ThreadPool(3)

# open the urls in their own threads
# and return the results
results = pool.map(urllib2.urlopen, urls)

# close the pool and wait for the work to finish
pool.close()
pool.join()

print "time = ", time.time() - start_time