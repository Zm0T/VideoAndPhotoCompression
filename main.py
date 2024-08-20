import os
import time
import sys
from PIL import Image
import cv2
from tqdm import tqdm
import subprocess
import platform

IMAGE_FORMATS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.webp')
VIDEO_FORMATS = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_instruction():
    print("""
Инструкция по использованию программы сжатия фото и видео:

Подготовка к использованию:
1. Установите Python 3.7 или выше:
   - Скачайте с официального сайта: https://www.python.org/downloads/
   - При установке на Windows отметьте галочку "Add Python to PATH"

2. Установите необходимые библиотеки. Откройте командную строку или терминал и выполните:
   pip install Pillow opencv-python tqdm

3. Установите FFmpeg:
   - Windows:
     a. Скачайте FFmpeg с https://ffmpeg.org/download.html
     b. Распакуйте архив и добавьте путь к папке bin в системную переменную PATH
   - macOS:
     a. Установите Homebrew с https://brew.sh/
     b. Выполните команду: brew install ffmpeg
   - Linux:
     Выполните команду: sudo apt-get install ffmpeg (для Ubuntu/Debian)
     или: sudo yum install ffmpeg (для CentOS/Fedora)

Использование программы:
1. Выберите тип файлов для сжатия (фото или видео).
2. Выберите уровень сжатия (низкий, средний, высокий).
3. Введите путь к папке с файлами для сжатия.
4. Программа создаст новую папку с сжатыми файлами внутри исходной папки.
5. После завершения сжатия вы увидите статистику и сможете выбрать, хотите ли вы сжать еще файлы.

Примечания:
- Для фото поддерживаются форматы: PNG, JPG, JPEG, TIFF, BMP, GIF, WebP.
- Для видео поддерживаются форматы: MP4, AVI, MOV, MKV, FLV, WMV.
- Время сжатия - приблизительное и может варьироваться в зависимости от характеристик вашего компьютера.
- Убедитесь, что у вас достаточно свободного места на диске для сохранения сжатых файлов.

Приятного использования!
    """)
    input("Нажмите Enter, чтобы продолжить...")

def compress_image(input_path, output_path, quality):
    try:
        with Image.open(input_path) as img:
            output_format = os.path.splitext(output_path)[1].lower()
            if output_format in ['.jpg', '.jpeg']:
                img.save(output_path, quality=quality, optimize=True)
            elif output_format in ['.png', '.webp']:
                img.save(output_path, optimize=True)
            else:
                img.save(output_path)
        return True
    except Exception as e:
        print(f"Ошибка при сжатии изображения {input_path}: {str(e)}")
        return False

def compress_video(input_path, output_path, crf):
    try:
        ffmpeg_command = ['ffmpeg', '-i', input_path, '-vcodec', 'libx264', '-crf', str(crf), output_path]
        if platform.system() == 'Windows':
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при сжатии видео {input_path}: {e.stderr.decode()}")
        return False

def get_video_duration(file_path):
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    cap.release()
    return duration

def estimate_compression_time(file_paths, file_type, compression_level):
    if file_type == "image":
        return len(file_paths) * 0.5  # Примерно 0.5 секунды на изображение
    else:  # video
        total_duration = sum(get_video_duration(file_path) for file_path in file_paths)
        compression_factor = {'1': 0.7, '2': 1.0, '3': 1.3}[compression_level]
        return total_duration * compression_factor

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        print("Неверный ввод. Пожалуйста, попробуйте снова.")

def get_valid_path(prompt):
    while True:
        path = input(prompt).strip().strip("\"'")
        if os.path.exists(path):
            return path
        print("Указанный путь не существует. Пожалуйста, попробуйте снова.")

def get_files_in_folder(folder_path, file_type):
    extensions = IMAGE_FORMATS if file_type == "image" else VIDEO_FORMATS
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(extensions)]

def main():
    while True:
        print("\nВыберите действие:")
        print("1. Инструкция")
        print("2. Сжать файлы")
        print("3. Выход")
        action = get_valid_input("Введите номер действия (1, 2 или 3): ", ['1', '2', '3'])

        if action == '1':
            clear_console()
            show_instruction()
            continue
        elif action == '3':
            print("Программа завершена.")
            break

        clear_console()
        print("Выберите тип файлов для сжатия:")
        print("1. Фото")
        print("2. Видео")
        choice = get_valid_input("Введите номер (1 или 2): ", ['1', '2'])

        clear_console()

        if choice == "1":
            file_type = "image"
            print("\nВыберите уровень сжатия для фото:")
            print("1. Низкий (качество 80)")
            print("2. Средний (качество 60) - Оптимальный")
            print("3. Высокий (качество 40)")
            compression_level = get_valid_input("Введите номер (1, 2 или 3): ", ['1', '2', '3'])
            quality = {"1": 80, "2": 60, "3": 40}[compression_level]
        else:
            file_type = "video"
            print("\nВыберите уровень сжатия для видео:")
            print("1. Низкий (CRF 23)")
            print("2. Средний (CRF 28) - Оптимальный")
            print("3. Высокий (CRF 33)")
            compression_level = get_valid_input("Введите номер (1, 2 или 3): ", ['1', '2', '3'])
            crf = {"1": 23, "2": 28, "3": 33}[compression_level]

        clear_console()

        input_folder = get_valid_path("Введите путь к папке с файлами для сжатия: ")
        output_folder = os.path.join(input_folder, f"compressed_{os.path.basename(input_folder)}")

        os.makedirs(output_folder, exist_ok=True)

        files = get_files_in_folder(input_folder, file_type)
        total_files = len(files)

        if total_files == 0:
            print(f"В указанной папке нет подходящих файлов для сжатия ({file_type}).")
            continue

        estimated_time = estimate_compression_time(files, file_type, compression_level)
        print(f"\nНайдено файлов для сжатия: {total_files}")
        print(f"Примерное время сжатия: {estimated_time:.2f} секунд")

        start_time = time.time()

        compressed_files = 0
        for file in tqdm(files, desc="Обработка файлов"):
            output_path = os.path.join(output_folder, os.path.basename(file))

            if file_type == "image":
                if compress_image(file, output_path, quality):
                    compressed_files += 1
            else:  # video
                if compress_video(file, output_path, crf):
                    compressed_files += 1

        end_time = time.time()
        print(f"\nСжатие завершено за {end_time - start_time:.2f} секунд")
        print(f"Успешно сжато файлов: {compressed_files} из {total_files}")

        another = get_valid_input("Хотите выполнить еще одно сжатие? (да/нет): ", ['да', 'нет'])
        if another != 'да':
            print("Программа завершена.")
            break

        clear_console()

if __name__ == "__main__":
    main()
