#ifndef COMMON_HPP_D2X
#define COMMON_HPP_D2X

#include <iostream>
#include <string>

#include <d2x/honly_logger.hpp>

#define d2x_assert(expr) \
{ \
    if (!(expr)) { \
        HONLY_LOGW("❌ | %s", #expr); \
    } else { \
        HONLY_LOGI_P("✅ | %s", #expr); \
    } \
}

#define d2x_assert_eq(a, b) \
{ \
    if (a != b) {\
        HONLY_LOGW("❌ | %s == %s (%s == %s)", \
            #a, #b, std::to_string(a).c_str(), std::to_string(b).c_str()); \
    } else {\
        HONLY_LOGI_P("✅ | %s == %s (%s == %s)", \
            #a, #b, std::to_string(a).c_str(), std::to_string(b).c_str()); \
    } \
}

#define D2X_WAIT HONLY_LOGW("🥳 Delete the D2X_WAIT to continue...");
#define D2X_YOUR_ANSWER  HONLY_LOGW("❌ | Please fill in your answer here to replace D2X_YOUR_ANSWER!");

#endif