// mcpp-standard: https://github.com/Sunrisepeak/mcpp-standard
// license: Apache-2.0
// file: dslings/cpp11/00-auto-and-decltype-3.cpp
//
// Exercise: cpp11 | 00 - auto and decltype | Function Return Type Deduction
//
// Tips: Use auto and decltype to fix errors in the code
//
// Docs:
//   - https://en.cppreference.com/w/cpp/language/auto
//   - https://en.cppreference.com/w/cpp/language/decltype
//   - https://github.com/Sunrisepeak/mcpp-standard/blob/main/book/src/cpp11/00-auto-and-decltype.md
//
// Exercise discussion: http://forum.d2learn.org/post/357
//
// Auto-Checker command:
//
//   d2x checker auto-and-decltype-3
//

#include <d2x/common.hpp>

#include <iostream>
#include <vector>

// 3. Function return types

auto add_func(int a, double b) -> decltype(a + b) {
    return a + b;
}

template<typename T1, typename T2>
D2X_YOUR_ANSWER minus_func(T1 a, T2 b) -> D2X_YOUR_ANSWER {
    return a - b;
}

int main() {

    d2x_assert_eq(minus_func(1, 2), -1);
    d2x_assert_eq(minus_func(2, 1), 1);
    d2x_assert_eq(minus_func(1, 2.1), -1.1);

    D2X_WAIT

    return 0;
}