from skimage import io


def str2bin(s):
    return ''.join(format(ord(i), '08b') for i in s)


def embed_message(image_path, message):
    # Load image
    img = io.imread(image_path)

    # Convert message to binary
    binary_message = str2bin(message)

    # Get the size of the message
    message_size = len(binary_message)

    # Check if the message can be embedded in the image
    if img.shape[0] * img.shape[1] * 3 < message_size:
        print('Error: message is too long to embed in the image')
        return

    # Embed the message in the image
    index = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                if index < message_size:
                    img[i, j, k] = (img[i, j, k] & ~1) | int(binary_message[index])
                    index += 1
                else:
                    break

            if index >= message_size:
                break

        if index >= message_size:
            break

    # Save the modified image
    io.imsave('embedded_image.bmp', img)


def extract_message(embedded_image_path):
    # Load the embedded image
    img = io.imread(embedded_image_path)

    # Extract the message from the image
    binary_message = ''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_message += str(img[i, j, k] & 1)

    # Convert binary message to string
    message = ''
    for i in range(0, len(binary_message), 8):
        symbol = chr(int(binary_message[i:i + 8], 2))
        if symbol != '\0':
            message += chr(int(binary_message[i:i + 8], 2))
        else:
            break

    return message


if __name__ == '__main__':
    message = input("Введите сообщение для внедрения: ")
    embed_message('image.bmp', message + '\0')

    message = extract_message('embedded_image.bmp')
    print(message)
