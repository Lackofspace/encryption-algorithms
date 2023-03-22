#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

string generate_key(int length) {
    string key;
    srand(time(nullptr)); // Инициализируем генератор случайных чисел
    for (int i = 0; i < length; i++) {
        int random_num = rand() % 26; // Генерируем случайное число от 0 до 25
        char c = random_num + 'A'; // Преобразуем число в символ и добавляем его к ключу
        key += c;
    }
    return key;
}

string vernam_encrypt(string plaintext, string key) {
    string ciphertext;
    for (int i = 0; i < plaintext.length(); i++) {
        char c = ((plaintext[i] - 'A') ^ (key[i] - 'A')) + 'A';
        ciphertext += c;
    }
    return ciphertext;
}

string vernam_decrypt(string ciphertext, string key) {
    string plaintext;
    for (int i = 0; i < ciphertext.length(); i++) {
        char c = ((ciphertext[i] - 'A') ^ (key[i] - 'A')) + 'A';
        plaintext += c;
    }
    return plaintext;
}

int main() {
    string plaintext, key;
    cout << "Enter plaintext:";
    getline(cin, plaintext);
    key = generate_key(plaintext.length());
    string ciphertext = vernam_encrypt(plaintext, key);
    cout << "Ciphertext:" << ciphertext << endl;
    string decryptedtext = vernam_decrypt(ciphertext, key);
    cout << "Decryptedtext:" << decryptedtext << endl;
    return 0;
}
