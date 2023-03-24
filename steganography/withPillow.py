# pip install pillow
from PIL import Image

def text_to_bits(text):
    """Преобразование входного сообщения в двоичный вид"""
    bits = []
    for char in text:
        binary = bin(ord(char))[2:].zfill(8)
        bits.extend(binary)
    return bits

def encode_lsb(image_path, secret_message):
    """Функция внедрения сообщения"""
    # Открываем изображение
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Преобразуем сообщение в двоичный вид
    secret_bits = text_to_bits(secret_message)

    # Проверяем, достаточно ли битов в изображении для хранения сообщения
    max_bits = width * height * 3
    if len(secret_bits) > max_bits:
        raise ValueError("Слишком большое сообщение для внедрения в это изображение")

    # Встраиваем сообщение
    bit_index = 0
    for y in range(height):
        for x in range(width):
            # Получаем значения RGB для текущего пикселя
            r, g, b = pixels[x, y]

            # Заменяем младшие биты каждого цветового канала на биты сообщения
            if bit_index < len(secret_bits):
                r = (r & ~1) | int(secret_bits[bit_index])
                bit_index += 1
            if bit_index < len(secret_bits):
                g = (g & ~1) | int(secret_bits[bit_index])
                bit_index += 1
            if bit_index < len(secret_bits):
                b = (b & ~1) | int(secret_bits[bit_index])
                bit_index += 1

            # Записываем измененные значения RGB в пиксель
            pixels[x, y] = (r, g, b)

            # Если сообщение уже внедрено, выходим из функции
            if bit_index >= len(secret_bits):
                return img

    # Если сообщение не влезло в изображение, выводим сообщение об ошибке
    raise ValueError("Недостаточно места для внедрения сообщения в это изображение")

def decode_lsb(image_path):
    """Функция извлечения внедренного сообщения"""
    # Открываем изображение
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    # Извлекаем биты сообщения
    secret_bits = []
    for y in range(height):
        for x in range(width):
            # Получаем значения RGB для текущего пикселя
            r, g, b = pixels[x, y]

            # Извлекаем младшие биты каждого цветового канала
            secret_bits.append(r & 1)
            secret_bits.append(g & 1)
            secret_bits.append(b & 1)

    # Преобразуем биты в символы
    secret_message = ""
    for i in range(0, len(secret_bits), 8):
        byte = secret_bits[i:i+8]
        char = chr(int("".join([str(bit) for bit in byte]), 2))
        # Конец вводимого сообщения
        if char == '\0':
            break
        secret_message += char


    return secret_message


if __name__ == "__main__":
    # Внедряем сообщение в изображение
    image_path = "image.bmp"
    secret_message = input("Input message: ") + '\0'
    encoded_image = encode_lsb(image_path, secret_message)
    encoded_image.save("encoded_image.bmp")

    # Извлекаем сообщение из изображения
    decoded_message = decode_lsb("encoded_image.bmp")
    print(decoded_message)
