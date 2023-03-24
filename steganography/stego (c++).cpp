#include <iostream>
#include <fstream>
#include <string>
#include <bitset>
#include <regex>

using namespace std;

// Функция для чтения BMP-изображения
int readBMP(const char* filename, unsigned char*& imgData, int& imgWidth, int& imgHeight) {
    ifstream file(filename, ios::in | ios::binary);
    if (!file) {
        cerr << "Failed to open BMP file" << endl;
        return 1;
    }

    // BMP заголовок
    char header[54];
    file.read(header, 54);
    if (header[0] != 'B' || header[1] != 'M') {
        cerr << "Invalid BMP file" << endl;
        return 1;
    }

    // Размер изображения и место начала данных изображения
    int imgOffset = *(int*)&header[10];
    int imgSize = *(int*)&header[34];
    imgWidth = *(int*)&header[18];
    imgHeight = *(int*)&header[22];

    // Выделение памяти для данных изображения и чтение их
    imgData = new unsigned char[imgSize];
    file.seekg(imgOffset, ios::beg);
    file.read((char*)imgData, imgSize);
    file.close();
    return imgSize;
}


// Функция для записи BMP-изображения
void writeBMP(const char* filename, unsigned char* imgData, int imgWidth, int imgHeight) {
    ofstream file(filename, ios::out | ios::binary);
    if (!file) {
        cerr << "Failed to open file for writing" << endl;
        return;
    }

    // BMP заголовок
    char header[54];
    header[0] = 'B';
    header[1] = 'M';
    *(int*)&header[2] = 54 + imgWidth * imgHeight * 3;
    *(int*)&header[10] = 54;
    *(int*)&header[14] = 40;
    *(int*)&header[18] = imgWidth;
    *(int*)&header[22] = imgHeight;
    *(short*)&header[26] = 1;
    *(short*)&header[28] = 24;
    *(int*)&header[34] = imgWidth * imgHeight * 3;
    file.write(header, 54);

    // Запись данных изображения
    file.write((char*)imgData, imgWidth * imgHeight * 3);
    file.close();
}

// Функция для преобразования строки в двоичный вид
string toBinary(string str) {
    string binary;
    for (char& c : str) {
        binary += bitset<8>(c).to_string();
    }
    return binary;
}

// Функция для внедрения битов в младшие разряды цветовых компонентов пикселей
void embedMessage(unsigned char* imgData, int imgSize, string message) {
    int pixelIndex = 0; // Индекс текущего пикселя
    int bitIndex = 0; // Индекс текущего бита в сообщении
    int messageLength = message.length();

    // Пока не внедрено все сообщение и не достигнут конец изображения
    while (bitIndex < messageLength && pixelIndex < imgSize / 3) {
        // Выделение цветовых компонент текущего пикселя
        unsigned char red = imgData[pixelIndex * 3];
        unsigned char green = imgData[pixelIndex * 3 + 1];
        unsigned char blue = imgData[pixelIndex * 3 + 2];

        // Внедрение битов в младшие разряды цветовых компонент
        if (bitIndex < messageLength) {
            // Выбор бита сообщения для внедрения
            char bit = message[bitIndex];

            // Внедрение бита в младший разряд красной компоненты
            red = (red & 0xFE) | bit;
            bitIndex++;

            if (bitIndex < messageLength) {
                // Выбор следующего бита сообщения для внедрения
                bit = message[bitIndex];

                // Внедрение бита в младший разряд зеленой компоненты
                green = (green & 0xFE) | bit;
                bitIndex++;
            }

            if (bitIndex < messageLength) {
                // Выбор следующего бита сообщения для внедрения
                bit = message[bitIndex];

                // Внедрение бита в младший разряд синей компоненты
                blue = (blue & 0xFE) | bit;
                bitIndex++;
            }
        }

        // Запись обновленных цветовых компонент в память
        imgData[pixelIndex * 3] = red;
        imgData[pixelIndex * 3 + 1] = green;
        imgData[pixelIndex * 3 + 2] = blue;

        // Переход к следующему пикселю
        pixelIndex++;
    }

    if (bitIndex < messageLength) {
        cerr << "Message is too large to embed in the image" << endl;
    }
}

// Функция для извлечения битов из младших разрядов цветовых компонент пикселей
string extractMessage(const unsigned char* imgData, int imgSize) {
    string binary;
    int pixelIndex = 0; // Индекс текущего пикселя

    // Пока не достигнут конец изображения
    while (pixelIndex < imgSize / 3) {
        // Выделение цветовых компонент текущего пикселя
        unsigned char red = imgData[pixelIndex * 3];
        unsigned char green = imgData[pixelIndex * 3 + 1];
        unsigned char blue = imgData[pixelIndex * 3 + 2];

        // Извлечение битов из младших разрядов цветовых компонент
        string bit = to_string(red & 1);
        binary += bit;

        bit = to_string(green & 1);
        binary += bit;

        bit = to_string(blue & 1);
        binary += bit;

        // Переход к следующему пикселю
        pixelIndex++;
    }

    // Преобразование двоичной строки в исходное сообщение
    string message;
    regex binary_regex("[01]{8}");

    for (int i = 0; i < binary.length(); i += 8) {
        string byteStr = binary.substr(i, 8);
        if (!regex_match(byteStr, binary_regex)) {
            cerr << "Error: byteStr is not a valid binary string with length 8" << std::endl;
            return "error";
        }
        char byte = (char)bitset<8>(byteStr).to_ulong();
        // Только символы, вводимые с клавиатуры
        if (byte < 32 || byte > 126){
            break;
        }
        message += byte;
    }
    return message;
}

// Пример использования функций внедрения и извлечения
int main() {
    // Загрузка изображения из файла
    const char *filename = "image.bmp";
    unsigned char* imgData;
    int imgWidth, imgHeight;
    int imgSize = readBMP(filename, imgData, imgWidth, imgHeight);

    // Ввод сообщения для внедрения
    cout << "Enter message to embed:";
    string message;
    getline(cin, message);
    message += "\n";
    // Преобразование сообщения в двоичную строку
    string binary = toBinary(message);

    // Внедрение сообщения в изображение
    embedMessage(imgData, imgSize, binary);

    // Сохранение модифицированного изображения в новый файл
    writeBMP("modified.bmp", imgData, imgWidth, imgHeight);

    // Извлечение сообщения из модифицированного изображения
    unsigned char* imgData1;
    int imgWidth1, imgHeight1;
    int imgSize1 = readBMP("modified.bmp", imgData1, imgWidth1, imgHeight1);

    string extracted = extractMessage(imgData1, imgSize1);

    // Вывод извлеченного сообщения
    cout << "Extracted message:" << extracted << endl;

    // Освобождение памяти
    delete[] imgData;

    return 0;
}
