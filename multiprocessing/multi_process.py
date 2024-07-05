import multiprocessing as mp
import time

def task_list(number, _list):
    time.sleep(5)
    _list.append(number)
    return "Task {} completed".format(number)

def worker_list(number,_list, result_queue):
    result = task_list(number, _list)
    result_queue.put(result)

def task(number):
    time.sleep(5)
    return "Task {} completed".format(number)

def worker(number, result_queue):
    result = task(number)
    result_queue.put(result)

def main():

    processes = []
    _list = []
    result_queue = mp.Queue()

    for i in range(1, 6):
        process = mp.Process(target=worker_list, args=(i, _list, result_queue))
        processes.append(process)
        process.start()
        print(process.pid)

    print('all start')
    for process in processes:
        process.join()
    print(_list)
    print('all finish')
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    print(_list)
    for result in results:
        print(result)



if __name__ == "__main__":
    main()
