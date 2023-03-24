import steganography

# Внедряем сообщение
message = input("Your message: ")
steganography.encode_lsb("image.bmp", message)

# Извлекаем сообщение
message_decoded = steganography.decode_lsb("image_decoded.bmp")
print(message_decoded)
