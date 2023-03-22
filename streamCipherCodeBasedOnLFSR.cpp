#include <iostream>
#include <string>
#include <vector>

using namespace std;

class LCG {
private:
    long long m;
    long long a;
    long long c;
    long long state;

public:
    LCG(long long m, long long a, long long c, long long seed) : m(m), a(a), c(c), state(seed) {}

    long long rand() {
        state = (a * state + c) % m;
        return state;
    }
};

string encrypt(const string& msg, LCG& lcg, vector<int>& key) {
    string result;
    for (int i = 0; i < msg.size(); ++i) {
        key[i] = lcg.rand() & 0xff;
        char c = ((msg[i] - 'A') ^ (key[i]))  + 'A';
        result += c;
    }
    return result;
}

string decrypt(const string& msg, vector<int> key) {
    string result;
    for (int i = 0; i < msg.size(); ++i) {
        char c = ((msg[i] - 'A') ^ (key[i]))  + 'A';
        result += c;
    }
    return result;
}

int main() {
    long long m = 1ull << 32;
    long long a = 1664525;
    long long c = 1013904223;
    long long seed = 12345;

    LCG lcg(m, a, c, seed);

    string msg;
    cout << "Enter a message:";
    getline(cin, msg);
    vector<int> key(msg.size());
    string encrypted = encrypt(msg, lcg, key);
    cout << "Encrypted message:" << encrypted << endl;



    string decrypted = decrypt(encrypted, key);
    cout << "Decrypted message:" << decrypted << endl;

    return 0;
}
