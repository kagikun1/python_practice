import time
from multiprocessing import Pool, Manager, Value
import os

def func(num, cnt):
    num.value = pow(2, cnt.value)
    print(f'Worker pid={os.getpid()}, ppid={os.getppid()}')

def run(num, cnt):
    count = 60
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
    print("------MultiProcess------")
    start = time.time()
    with Pool(processes=work) as pool:
        manager = Manager()
        num = manager.Value('d', num.value)
        cnt = manager.Value('d', cnt.value)
        results = []
        for i in range(count):
            cnt.value = i
            results.append(pool.apply_async(func, (num, cnt)))
        for result in results:
            result.get()
    print(f"処理時間：{time.time() - start}")
    print(f'[{num.value}]')

if __name__ == '__main__':
    num = Value('d', 2)
    cnt = Value('d', 0)

    run(num, cnt)