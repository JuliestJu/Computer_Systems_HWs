import threading
import multiprocessing
import os
import time
from collections import defaultdict
from queue import Queue

def search_keywords_in_files(file_list, keywords, queue):
    results = defaultdict(list)
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                for keyword in keywords:
                    if keyword in text:
                        results[keyword].append(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    queue.put(results)

def merge_results(queue, num_workers):
    merged_results = defaultdict(list)
    for _ in range(num_workers):
        results = queue.get()
        for keyword, files in results.items():
            merged_results[keyword].extend(files)
    return dict(merged_results)

def multithreaded_keyword_search(file_paths, keywords, num_threads):
    file_chunks = [file_paths[i::num_threads] for i in range(num_threads)]
    results_queue = Queue()
    threads = []

    for chunk in file_chunks:
        thread = threading.Thread(target=search_keywords_in_files, args=(chunk, keywords, results_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return merge_results(results_queue, num_threads)

def multiprocess_keyword_search(file_paths, keywords, num_processes):
    file_chunks = [file_paths[i::num_processes] for i in range(num_processes)]
    results_queue = multiprocessing.Queue()
    processes = []

    for chunk in file_chunks:
        process = multiprocessing.Process(target=search_keywords_in_files, args=(chunk, keywords, results_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return merge_results(results_queue, num_processes)

def main():
    file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
    keywords = ['keyword1', 'keyword2', 'keyword3']
    num_workers = 2
    method = 'multiprocessing'

    start_time = time.time()

    if method == 'threading':
        results = multithreaded_keyword_search(file_paths, keywords, num_workers)
    elif method == 'multiprocessing':
        results = multiprocess_keyword_search(file_paths, keywords, num_workers)
    else:
        raise ValueError("Invalid method. Choose 'threading' or 'multiprocessing'.")

    end_time = time.time()

    for keyword, files in results.items():
        print(f"Keyword: {keyword}")
        for file_path in files:
            print(f"  Found in: {file_path}")

    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
