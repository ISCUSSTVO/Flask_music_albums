import os
import re
from transliterate import translit

def slugify_filename(filename):
    # Разделяем имя и расширение
    name, ext = os.path.splitext(filename)
    
    # 1. Переводим в нижний регистр
    name = name.lower()
    
    # 2. Транслитерация (кириллица -> латиница)
    try:
        name = translit(name, 'ru', reversed=True)
    except:
        pass # Если транслит не нужен, оставляем как есть
    
    # 3. Убираем лишние символы и меняем пробелы на _
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_-]+', '_', name)
    
    return name.strip('_') + ext.lower()

# Список папок для обработки
folders = ['static/img/artists', 'static/img/covers']

for folder in folders:
    if not os.path.exists(folder):
        print(f"Папка {folder} не найдена, пропускаю.")
        continue
        
    print(f"Обработка папки: {folder}")
    for filename in os.listdir(folder):
        old_path = os.path.join(folder, filename)
        
        # Пропускаем папки, работаем только с файлами
        if os.path.isfile(old_path):
            new_name = slugify_filename(filename)
            new_path = os.path.join(folder, new_name)
            
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Переименовано: {filename} -> {new_name}")

print("\nГотово! Теперь все файлы в нижнем регистре и без пробелов.")