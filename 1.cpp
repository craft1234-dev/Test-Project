#include <string>
#include <sstream>
#include <algorithm>
#include <cassert>

std::string reverse_words(const std::string &str) {
    std::istringstream iss(str);
    std::ostringstream result;
    std::string word;
    bool first = true;

    while (iss >> word) {
        if (!first) result << " ";
        first = false;

        std::string reversed_word;
        std::string current_segment;
        bool is_alphanumeric = false;

        for (char c : word) {
            if (std::isalnum(c)) {
                if (!is_alphanumeric) {
                    // Reverse previous non-alphanumeric segment
                    if (!current_segment.empty()) {
                        result << current_segment;
                        current_segment.clear();
                    }
                    is_alphanumeric = true;
                }
                current_segment.push_back(c);
            } else {
                if (is_alphanumeric) {
                    // Reverse alphanumeric segment
                    std::reverse(current_segment.begin(), current_segment.end());
                    result << current_segment;
                    current_segment.clear();
                    is_alphanumeric = false;
                }
                current_segment.push_back(c);
            }
        }

        // Handle last segment
        if (is_alphanumeric) {
            std::reverse(current_segment.begin(), current_segment.end());
        }
        result << current_segment;
    }

    return result.str();
}

int main() {
    std::string test_str = "String; 2be reversed...";
    assert(reverse_words(test_str) == "gnirtS; eb2 desrever...");
    return 0;
}