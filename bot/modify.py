__all__ = ['draw_image', 'calculate_font_size']

import random
from PIL import Image, ImageDraw, ImageFont

from os import listdir
from os.path import isfile, join


def calculate_font_size(text: str, font_path: str, column_width: int) -> int:
    font_size = 1
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(text)[0]  # type: ignore
    while text_width < column_width:
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
        text_width = font.getsize(text)[0]  # type: ignore
    font_size -= 1
    return font_size


def draw_image(text_img: str, shad: str) -> str:

    # take list all files of a directory
    only_files = [f for f in listdir(r'storage\image') if isfile(
        join(r'storage\image', f))]

    front = 'storage\core\pixelfont_7.ttf'
    image = Image.open(
        r'storage\core\only_text.png')
    font = ImageFont.truetype(
        front, calculate_font_size(text_img, front, 1000))
    inserted_image = Image.open(
        fr"storage\image\{random.choice(only_files)}")

    width, height = image.size
    text_bbox = ImageDraw.Draw(image).textbbox((0, 0), text_img, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1] + 70

    # Вычисляем координаты размещения изображения по центру
    x = 1500 + random.randint(10, 40)
    y = 500 + random.randint(10, 100)

    # Размещаем изображение по центру
    image.paste(inserted_image, (x, y, x + inserted_image.width,
                y + inserted_image.height), mask=inserted_image)
    x = 50 + random.randint(10, 40)
    y = 500 + random.randint(10, 200)
    image.paste(inserted_image, (x, y, x + inserted_image.width,
                y + inserted_image.height), mask=inserted_image)

    # Размещаем текст по центру
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw = ImageDraw.Draw(image)
    draw.text((text_x, text_y), text_img, fill=(255, 255, 255), font=font)
    font = ImageFont.truetype(
        front, calculate_font_size(text_img, front, 1000)//2)
    draw.text((text_x+350, text_y+150), shad, fill=(255, 255, 255), font=font)

    result_path = fr'storage\temp\image_{text_img}.jpg'
    image.save(result_path)
    return result_path
