# Программа для сжатия фото и видео

Эта программа позволяет сжимать фотографии и видео файлы с различными уровнями компрессии. Она поддерживает несколько форматов изображений и видео, и работает на Windows, macOS и Linux.

## Возможности

- Сжатие фотографий (PNG, JPG, JPEG, TIFF, BMP, GIF, WebP)
- Сжатие видео (MP4, AVI, MOV, MKV, FLV, WMV)
- Три уровня сжатия для фото и видео
- Оценка времени сжатия
- Удобный интерфейс командной строки
- Кроссплатформенность (Windows, macOS, Linux)

## Требования

- Python 3.7 или выше
- Pillow
- OpenCV-Python
- tqdm
- FFmpeg

## Установка

1. Убедитесь, что у вас установлен Python 3.7 или выше. Скачать Python можно [здесь](https://www.python.org/downloads/).

2. Склонируйте репозиторий:
   ```
   git clone https://github.com/Zm0T/VideoAndPhotoCompression.git
   cd photo-video-compressor
   ```

3. Установите необходимые библиотеки:
   ```
   pip install Pillow opencv-python tqdm
   ```

4. Установите FFmpeg:
   - Windows: 
     - Скачайте FFmpeg с [официального сайта](https://ffmpeg.org/download.html)
     - Распакуйте архив и добавьте путь к папке bin в системную переменную PATH
   - macOS:
     - Установите [Homebrew](https://brew.sh/), затем выполните:
       ```
       brew install ffmpeg
       ```
   - Linux:
     - Ubuntu/Debian:
       ```
       sudo apt-get install ffmpeg
       ```
     - CentOS/Fedora:
       ```
       sudo yum install ffmpeg
       ```

## Использование

1. Запустите программу:
   ```
   python main.py
   ```

2. Следуйте инструкциям в консоли:
   - Выберите тип файлов для сжатия (фото или видео)
   - Выберите уровень сжатия
   - Укажите путь к папке с файлами для сжатия

3. Программа создаст новую папку с сжатыми файлами внутри исходной папки.

## Примечания

- Время сжатия является приблизительным и может варьироваться в зависимости от характеристик вашего компьютера.
- Убедитесь, что у вас достаточно свободного места на диске для сохранения сжатых файлов.
