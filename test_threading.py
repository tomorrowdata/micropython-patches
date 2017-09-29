

import time as time
import threading
from queue import Queue


def isodatetime():
	return '{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}'.format(*time.localtime(time.time())[:6])

def threadlog(*args):
    print(threading.current_thread(), isodatetime(), *args)
    
    

def a(q):
    for i in range(4):
        q.put(i)
        threadlog('enqueue', i)
        time.sleep(1)
    threadlog('finished iterations, exiting.')


def b(q):
    while True:
        i = q.get(block=True)

        if i is None:
            threadlog('received stop message, exiting.')
            break

        threadlog('dequeue', i)

threadlog('Started.')

q = Queue()

t1 = threading.Thread(name='t1', target=a, args=(q,))
t2 = threading.Thread(name='t2', target=b, args=(q,))

t1.start()
t2.start()

t1.join()

q.put(None)

t2.join()

threadlog('finished.')

