# pip install opencv-python
import cv2
import numpy as np


def encode_lsb(image_path, secret_message):
    # Загружаем изображение и конвертируем его в формат NumPy массива
    img = cv2.imread(image_path)
    img = np.array(img)

    # Конец строки
    secret_message += '\0'

    # Преобразуем сообщение в список битов
    secret_bits = [int(bit) for char in secret_message for bit in '{0:08b}'.format(ord(char))]

    # Проверяем, что сообщение может быть внедрено в изображение
    if len(secret_bits) > img.shape[0] * img.shape[1] * 3:
        raise ValueError("Слишком длинное сообщение для данного изображения")

    # Внедряем биты сообщения в изображение
    bit_idx = 0
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            for color in range(3):
                # Извлекаем значение текущего бита и бита цветовой компоненты
                if bit_idx < len(secret_bits):
                    bit = secret_bits[bit_idx]
                    color_bit = img[row, col, color] & 1

                    # Если биты не совпадают, меняем младший бит цветовой компоненты
                    if bit != color_bit:
                        img[row, col, color] ^= 1

                    bit_idx += 1

                # Если все биты сообщения были внедрены, прекращаем цикл
                if bit_idx == len(secret_bits):
                    break

            if bit_idx == len(secret_bits):
                break

        if bit_idx == len(secret_bits):
            break

    # Сохраняем измененное изображение
    cv2.imwrite("image_decoded.bmp", img)


def decode_lsb(image_path):
    # Загружаем изображение и конвертируем его в формат NumPy массива
    img = cv2.imread(image_path)
    img = np.array(img)

    # Извлекаем биты сообщения
    secret_bits = []
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            for color in range(3):
                # Извлекаем младший бит цветовой компоненты
                bit = img[row, col, color] & 1
                secret_bits.append(bit)

    # Преобразуем биты в сообщение
    secret_message = ''.join(
        [chr(int(''.join(map(str, secret_bits[i:i + 8])), 2)) for i in range(0, len(secret_bits), 8)])

    # Удаляем все символы после символа '\0'
    secret_message = secret_message.split('\0')[0]

    return secret_message



