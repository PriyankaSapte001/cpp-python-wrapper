#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <cstdlib>

// Simple C++ CLI tool:
// Reads integers (one per line) from --input <file>
// Prints "SUM=<sum>" to stdout
// Exit codes:
// 0 = OK (sum >= threshold)
// 1 = input/file/parse error
// 2 = sum below threshold
// Usage: tool --input <file> --threshold <int>
int main(int argc, char* argv[]) {
    std::string inputPath;
    long long threshold = 0;
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--input" && i + 1 < argc) {
            inputPath = argv[++i];
        } else if (arg == "--threshold" && i + 1 < argc) {
            threshold = std::atoll(argv[++i]);
        }
    }
    if (inputPath.empty()) {
        std::cerr << "Missing --input\n";
        return 1;
    }
    std::ifstream in(inputPath);
    if (!in.is_open()) {
        std::cerr << "Cannot open file: " << inputPath << "\n";
        return 1;
    }
    long long sum = 0;
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::istringstream iss(line);
        long long val;
        if (!(iss >> val)) {
            std::cerr << "Parse error on line: " << line << "\n";
            return 1;
        }
        sum += val;
    }
    std::cout << "SUM=" << sum << std::endl;
    if (sum >= threshold) return 0;
    return 2;
}
