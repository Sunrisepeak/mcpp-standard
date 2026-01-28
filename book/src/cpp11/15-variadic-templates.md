# 可变参数模板
## C++11之前如何处理可变参数
C++11引入可变参数模板之前,通常使用**宏**或者**模板递归展开**的方式处理可变参数,但是这两种方式都有一些限制:宏的语法复杂,模板递归展开的代码可读性差,并且都难以调试,拓展性差。

以实现一个支持任意参数的输出函数为例介绍这些用法。由于模板递归展开过于复杂,我们只介绍宏与模板生成的方式。

### 可变参数宏
> 继承自C语言,使用`...`表示宏定义的可变参数,使用`__VA_ARGS__`访问宏调用时传入的参数,使用`##__VA_ARGS__`(GCC拓展)处理零个参数的情况。

```cpp
#define LOG(fmt, ...)  printf(fmt, __VA_ARGS__)

LOG("x = %d, y = %f\n", 10, 3.14); // 展开为 printf("x = %d, y = %f\n", 10, 3.14);
LOG("Hello");  // 展开为 printf("Hello");
```

可变参数宏使用简单但场景受限,难以与现代C++代码结合:
- 无法实现类型安全检查
  - `LOG("%s", 42); // 编译通过,但运行时崩溃或输出垃圾:将42视为地址进行隐式类型转换`
- 无法处理引用、移动语义、无法保存参数包
  - `#define MAKE_SHARED(type, ...) std::shared_ptr<type>(new type(__VA_ARGS__))` 宏会将变量直接进行文本替换,无论如何都采用值传递的方式
  - 无法遍历`__VA_ARGS__`并对每个参数做不同处理

### 模板重载与硬编码
这是最直观也最笨拙的方法。手动为 1 个参数、2 个参数、3 个参数……直到N个参数分别编写重载版本。
这种做法缺点很明显: 代码冗余极大,维护困难,拓展性差。

### 宏与模板生成
`Boost.Preprocessor`广泛使用这种技巧,我们来模拟一下。
核心思路:让编译器自动生成如下代码:
- `template<typename T1> void print(T1 p1) { ... }`
- `template<typename T1, typename T2> void print(T1 p1, T2 p2) { ... }`
- `template<typename T1, typename T2,...,typename TN> void print(T1 p1, T2 p2,...,TN pN) { ... }`

> 第一步: 定义递归的终止点,即只有一个参数的情况
```cpp
// 生成模板参数: T1, T2, T3...
#define TP_PARAM(n) typename T##n
// 生成函数参数: T1 p1, T2 p2...
#define FN_PARAM(n) T##n p##n
// 生成打印语句: std::cout << p1 << p2...
#define PRINT_BODY(n) std::cout << p##n << " ";
```

> 第二步: 定义递归展开的模板
```cpp
// 模板参数声明逻辑
#define REPEAT_TP_1     TP_PARAM(1)
#define REPEAT_TP_2     REPEAT_TP_1, TP_PARAM(2)
#define REPEAT_TP_3     REPEAT_TP_2, TP_PARAM(3)

// 函数参数声明逻辑
#define REPEAT_FN_1     FN_PARAM(1)
#define REPEAT_FN_2     REPEAT_FN_1, FN_PARAM(2)
#define REPEAT_FN_3     REPEAT_FN_2, FN_PARAM(3)

// 基础打印逻辑
#define REPEAT_PRINT_1  PRINT_BODY(1)
#define REPEAT_PRINT_2  REPEAT_PRINT_1 PRINT_BODY(2)
#define REPEAT_PRINT_3  REPEAT_PRINT_2 PRINT_BODY(3)
```

> 第三步: 使用宏来生成函数
```cpp
#define DEFINE_LOG_FUNCTION(n) \
    template<REPEAT_TP_##n> \
    void log(REPEAT_FN_##n) { \
        REPEAT_PRINT_##n \
        std::cout << std::endl; \
    }

// 实际生成代码
DEFINE_LOG_FUNCTION(1)
DEFINE_LOG_FUNCTION(2)
DEFINE_LOG_FUNCTION(3)

// Expands to
template <typename T1, typename T2, typename T3>
void log(T1 p1, T2 p2, T3 p3) {
  std ::cout << p1 << " ";
  std ::cout << p2 << " ";
  std ::cout << p3 << " ";
  std ::cout << std ::endl;
}
```
显然,这种方式拓展性差并且编译速度慢,难以调试。

## 可变参数模板的用法
    千呼万唤始出来
C++11引入了可变参数模板,自此可以优雅地处理可变参数。示例代码如下
```cpp
// 递归终止函数
void print() { std::cout << std::endl; }

// 展开参数包的模板
template<typename T, typename... Args>
void print(T first, Args... args) {
    std::cout << first << " ";
    print(args...); // 递归调用，每次剥离一个参数
}

// print(1, "Hello", 3.14, 'A'); // 完美运行，类型安全
```
C++11之后,在模板中使用`...`来表示可变参数包。可以看到可变参数包一共在三个位置出现:
1. 在`template<typename T, typename... Args>`语句中,可变的是参数的类型,因此`...`修饰`typename`
2. 在`void print(T first, Args... args)`语句中,可变的是函数参数,因此`...`修饰`Args`
3. 在`print(args...)`语句中,可变的是参数包,因此`...`修饰`args`

可变参数模板可以和引用、移动语义结合使用。事实上,可变参数模板声明时通常和**万能引用**结合,以支持完美转发。
以简单的C++11 make_shared实现为例说明
```cpp
template <typename T, typename... Args>
std::shared_ptr<T> make_shared(Args&&... args) {
    T* ptr = new T(std::forward<Args>(args)...);
    return std::shared_ptr<T>(ptr);
}
```

> 缺陷与不足  

由于C++11没有直接遍历参数包的语法,通常采用递归方式处理可变参数包。递归终止函数通常为空函数,并且是非模板函数(C++决议时会优先使用同名的非模板函数)。
使用起来略微麻烦并且递归实际深度受限(编译器默认递归限制为1024)。

> 可变参数模板真正的大放光彩得等到C++17引入折叠表达式以及if constexpr

## 可变参数模板的增强
### C++14
C++14 对可变参数模板本身没有引入新的语法,但通过引入一些辅助工具和特性,增强了其可用性和表达能力。其中最重要的是 `std::index_sequence` 和 `std::make_index_sequence`。

`std::index_sequence` 是一个编译期整数序列,它允许在编译期生成一个包含 0 到 N-1 整数的序列。结合 `std::make_index_sequence`, 可以在编译期展开参数包,并对参数包中的每个元素执行操作,而无需依赖递归。这在需要按索引访问参数包时非常有用。

**使用 `std::index_sequence` 打印参数**
```cpp
template <typename T, std::size_t... Is>
void print_impl(T&& t, std::index_sequence<Is...>) {
    // 使用逗号表达式和初始化列表展开参数包，逐个打印
    ((std::cout << "Arg " << Is << ": " << std::get<Is>(std::forward<T>(t)) << std::endl), ...);
}

template <typename... Args>
void print_args(Args&&... args) {
    auto t = std::make_tuple(std::forward<Args>(args)...);
    // 生成一个与参数包大小匹配的 index_sequence
    print_impl(t, std::make_index_sequence<sizeof...(Args)>{});
}

// print_args(10, "Hello", 3.14);
// Arg 0: 10
// Arg 1: Hello
// Arg 2: 3.14
```
> 上述 `print_impl` 的 `((expression), ...)` 结构是为了在 C++14 中模拟 C++17 的折叠表达式行为。在 C++17 及更高版本中，可以直接使用折叠表达式简化此操作。

虽然 `std::index_sequence` 提供了非递归处理参数包的能力,但在实际使用中,其语法仍然相对复杂。C++17 的折叠表达式将大大简化这类操作。

### C++17
C++17 为可变参数模板带来了革命性的改进,主要通过引入**折叠表达式 (Fold Expressions)** 和 **`if constexpr`** 极大地简化了参数包的处理和编译期条件分支。

**折叠表达式 (Fold Expressions)**
折叠表达式提供了一种简洁的语法,可以将一个二元运算符应用于参数包中的所有元素。这使得对参数包进行求和、逻辑运算、连接字符串等操作变得非常直观,大大减少了递归模板的样板代码。

折叠表达式有四种形式:
- **一元左折叠:** `(... op pack)` 展开为 `((pack1 op pack2) op pack3) op ...`
- **一元右折叠:** `(pack op ...)` 展开为 `pack1 op (pack2 op (pack3 op ...))`
- **二元左折叠:** `(init op ... op pack)` 展开为 `(((init op pack1) op pack2) op pack3) op ...`
- **二元右折叠:** `(pack op ... op init)` 展开为 `pack1 op (pack2 op (pack3 op ... op init))`

二元表达式多了一个初始值

**使用折叠表达式**
```cpp
// 一元左折叠
template <typename... Args>
auto sub(Args... args) {
    return (... - args); // 展开为 ((arg1 - arg2) - arg3) ... - argN
}

// 一元右折叠
template <typename... Args>
auto sum(Args... args) {
    return (args + ...); // 展开为 arg1 + (arg2 + (arg3 + ...))
}

// 二元左折叠
template<typename T,typename... Args>
auto sub_with_init_left(T init, Args... args) {
    // (((init - args1) - args2) - ... - argsN)
    return (init - ... - args);
}

// 二元左折叠
template<typename T,typename... Args>
auto sum_with_init_right(T init, Args... args) {
    // (args1 + (args2 + ... + (argsN + init)))
    return (args + ... + init);
}
```

**`if constexpr`**
`if constexpr` 提供了编译期条件分支的能力。与运行时 `if` 语句不同, `if constexpr` 的条件在编译时求值,并且只有满足条件的那个分支才会被编译。这对于基于类型属性或编译期常量来生成不同代码路径的模板编程来说非常有用,可以有效替代 SFINAE 或标签分发等复杂技术,使代码更清晰、更易于维护。

**使用 `if constexpr` 进行编译期类型检查**
```cpp
template <typename T>
void process_value(T value) {
    if constexpr (std::is_integral_v<T>) { // 编译期检查是否为整数类型
        std::cout << "Processing integral value: " << value * 2 << std::endl;
    } else if constexpr (std::is_floating_point_v<T>) { // 编译期检查是否为浮点类型
        std::cout << "Processing floating point value: " << value * 1.5 << std::endl;
    } else {
        std::cout << "Processing other type: " << value << std::endl;
    }
}
// 不再需要同名函数 void process_args()来终止调用
template<typename... Args>
void process_args(T first_arg, Args... rest_args) {
    process_value(first_arg);
    if constexpr (sizeof...(rest_args) > 0) { // 编译期检查是否还有剩余参数
        process_args(rest_args...); // 递归调用处理剩余参数
    }
}

// process_args(10, 3.14, "hello", true); 
```
`if constexpr` 结合可变参数模板,可以实现非常灵活且类型安全的编译期多态行为。