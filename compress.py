import os
from PIL import Image
import shutil


def compress_images(source_dir, target_dir, qual):
    if os.path.isdir(source_dir):
        # проходим по всем файлам и папкам в исходной директории
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                target_path = os.path.join(target_dir, os.path.relpath(root, source_dir))
                # проверяем, является ли файл изображением
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', 'jfif')):
                    # создаем все директории, если они не существуют
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)
                    # открываем изображение
                    img = Image.open(os.path.join(root, file))
                    # конвертируем в формат jpg и сжимаем до минимального размера
                    img = img.convert("RGB")
                    img.save(os.path.join(target_path, file), format="JPEG", optimize=True, quality=qual)
                    yield str(file)
                else:
                    # копируем неизображения в целевую директорию если их не существует
                    if not os.path.exists(target_path):
                        os.makedirs(target_path)
                    shutil.copy(os.path.join(root, file), os.path.join(target_path, file))

        # если source_dir является файлом
    elif os.path.isfile(source_dir):
        # проверяем, является ли файл изображением
        if source_dir.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', 'jfif')):
            # создаем директорию, если она не существует
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            # открываем изображение
            img = Image.open(source_dir)
            # конвертируем в формат jpg и сжимаем до минимального размера
            img = img.convert("RGB")
            img.save(os.path.join(target_dir, os.path.basename(source_dir)), format="JPEG", optimize=True, quality=qual)
            yield str(source_dir)
    else:
        # выводим сообщение об ошибке
        yield ("Не корректный путь")


