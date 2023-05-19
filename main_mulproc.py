import time
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Value, Array, Queue
import sys
import os
import threading

def func(num, cnt):
    num.value = pow(2, cnt.value)
    #print(f'Worker pid={os.getpid()}, ppid={os.getppid()} thread={threading.current_thread().name}')

def run(num, cnt):
    count = 900
    work = 16

    print("------Normal------")
    start = time.time()
    for i in range(count):
        cnt.value = i
        func(num, cnt)
    print(f"処理時間：{time.time() - start}")
    print(f'[{num.value}]')
    
    num.value = 2
    cnt.value = 0
    print("------MultiThread------")
    start = time.time()
    with ThreadPoolExecutor(max_workers=work) as exec:
        for i in range(count):
            cnt.value = i
            exec.submit(func, num, cnt)
    print(f"処理時間：{time.time() - start}")
    print(f'[{num.value}]')

    cnt.value = 0
    num.value = 2
    print("------MultiProcess------")
    start = time.time()
    with ProcessPoolExecutor(max_workers=work) as exec:
        for i in range(count):
            cnt.value = i
            exec.submit(func(num, cnt))
    print(f"処理時間：{time.time() - start}")
    print(f'[{num.value}]')
    
if __name__ == '__main__':
    
    num = Value('d', 2)
    cnt = Value('d', 0)

    run(num, cnt)