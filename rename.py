import os
import re
from transliterate import translit

def slugify_filename(filename):

    name, ext = os.path.splitext(filename)

    name = name.lower()

    try:
        name = translit(name, 'ru', reversed=True)
    except:
        pass 

    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_-]+', '_', name)
    
    return name.strip('_') + ext.lower()


folders = ['static/img/artists', 'static/img/covers']

for folder in folders:
    if not os.path.exists(folder):
        print(f"Папка {folder} не найдена, пропускаю.")
        continue
        
    print(f"Обработка папки: {folder}")
    for filename in os.listdir(folder):
        old_path = os.path.join(folder, filename)

        if os.path.isfile(old_path):
            new_name = slugify_filename(filename)
            new_path = os.path.join(folder, new_name)
            
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Переименовано: {filename} -> {new_name}")

print("\nГотово! Теперь все файлы в нижнем регистре и без пробелов.")