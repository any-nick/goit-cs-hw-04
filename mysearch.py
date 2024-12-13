def search_keywords(file_paths, keywords, result_queue):
    results = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    positions = []
                    index = content.find(keyword)
                    while index != -1:
                        positions.append(index)
                        index = content.find(keyword, index + 1)
                    if positions:
                        results.setdefault(file_path, {})[keyword] = positions
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    result_queue.put(results)