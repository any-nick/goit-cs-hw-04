import os
from multiprocessing import Process, Queue
import pandas as pd
from mysearch import search_keywords

# Multiprocessing реалізація
def multiprocessing_search(file_paths, keywords, num_processes=4):
    process_list = []
    result_queue = Queue()
    chunk_size = len(file_paths) // num_processes + (len(file_paths) % num_processes > 0)

    for i in range(num_processes):
        chunk = file_paths[i * chunk_size:(i + 1) * chunk_size]
        process = Process(target=search_keywords, args=(chunk, keywords, result_queue))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()

    # Збираємо результати
    results = {}
    while not result_queue.empty():
        results.update(result_queue.get())

    return results

if __name__ == "__main__":
    folder_path = "./generated_files"
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    keywords = ["хліб", "гроші", "сміття"]

    multiprocessing_results = multiprocessing_search(file_paths, keywords)
    data = []
    for file, keywords in multiprocessing_results.items():
        for keyword, position in keywords.items():
            data.append([file, keyword, position])
    df = pd.DataFrame(data, columns=['File', 'Keyword', 'Position'])
    print(df)
