import os
import time
from threading import Thread
from queue import Queue
import pandas as pd
from mysearch import search_keywords

# Threading реалізація
def threading_search(file_paths, keywords, num_threads=4):
    thread_list = []
    result_queue = Queue()
    chunk_size = len(file_paths) // num_threads + (len(file_paths) % num_threads > 0)

    for i in range(num_threads):
        chunk = file_paths[i * chunk_size:(i + 1) * chunk_size]
        thread = Thread(target=search_keywords, args=(chunk, keywords, result_queue))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    # Збираємо результати
    results = {}
    while not result_queue.empty():
        results.update(result_queue.get())

    return results

if __name__ == "__main__":
    folder_path = "./generated_files"
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    keywords = ["хліб", "гроші", "сміття"]

    print("Starting threading search...")
    threading_results = threading_search(file_paths, keywords)
    data = []
    for file, keywords in threading_results.items():
        for keyword, position in keywords.items():
            data.append([file, keyword, position])
    df = pd.DataFrame(data, columns=['File', 'Keyword', 'Position'])
    print(df)