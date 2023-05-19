import time

def func1():
    time.sleep(3)
    return 'done'

def calc_time():
    start = time.time()
    result = func1()
    print(f' {time.time() - start} s')
    