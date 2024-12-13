import os
import random
from faker import Faker

fake = Faker('uk_UA')

output_folder = "fake_files"
os.makedirs(output_folder, exist_ok=True)

files_number = 26

for i in range(files_number):

    file_name = f"file_{i}.txt"
    file_path = os.path.join(output_folder, file_name)
    
    word_count = random.randint(500, 1000)
    text = fake.text(max_nb_chars=word_count * 3)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)
