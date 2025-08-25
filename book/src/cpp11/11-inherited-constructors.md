# 继承构造函数

继承构造函数是C++11 引入的一个语法特性 - 解决了在类继承结构中 派生类重复定义基类构造函数 的繁琐问题

| Book | Video | Code | X |
| --- | --- | --- | --- |
| [cppreference](https://en.cppreference.com/w/cpp/language/using_declaration.html#Inheriting_constructors) / [markdown](https://github.com/Sunrisepeak/mcpp-standard/blob/main/book/src/cpp11/11-inherited-constructors.md) | [视频解读]() | [练习代码]() |  |

**为什么引入?**

- 减少重复代码, 避免手动转发
- 提高代码的表达能力

## 一、基础用法和场景

### 复用基类的构造函数

在**继承构造函数**这个特性引入之前, 即使基类和派生的构造函数形式没有任何区别, 也需要重新定义, 然后通过手动把参数转发到基类, 这不仅造成了一定程度的代码重复, 而且也不够简洁。例如, 下面的`MyObject`就对每个`Base`中的构造函数做了重新实现

```cpp
class ObjectBase {
    //...
public:
    ObjectBase(int) {}
    ObjectBase(double) {}
};

class MyObject : public ObjectBase {
public:
    MyObject(int x) : ObjectBase(x) {}
    MyObject(double y) : ObjectBase(y) {}
    //...
};
```

而用这个特性, 通过`using ObjectBase::ObjectBase;`直接就可以继承基类中的构造函数, 不仅可以避免这个过程, 同代码也变的更简洁了

```cpp
class MyObject : public ObjectBase {
public:
    using ObjectBase::ObjectBase;
    //...
};
```

这里需要注意的是, **构造函数继承** 的编译期隐式代码生成, 不仅仅是对构造函数的"单纯"复制, 而且在派生类中还有类似"自动重命名的效果 `ObjectBase` -> `MyObject` "。即:

```cpp
class MyObject : public ObjectBase {
public:
    // 可能的生成代码
    MyObject(int x) : ObjectBase(x) {}
    MyObject(double y) : ObjectBase(y) {}
};
```

### 临时扩展功能用于测试

对一些类型做测试或调试时, 我们常常期望可以使用像`to_string()`之类的一些接口。如果不方便直接修改源代码, 这个时候 就可以使用 **继承构造函数** 的性质来追加一些方便调试的接口函数。例如下面有个`Student`类:

```cpp
class Student {
protected:
    //...
    double score;
public:
    string id;
    string name;
    uint age;

    Student(string id, string name);
    Student(string id, string name, uint age);
    Student(string id, ...);
};
```
在对其测试时, 通过实现`StudentTest`并增加一些辅助测试的函数, 这样更方便测试代码的编写。

```cpp
class StudentTest : public Student {
public:
    using Student::Student;

    std::string to_string() const {
        return "{ id: " + id + ", name: " + name
            + ", age: " + std::to_string(age) + " }";
    }

    void dump() const { /* 一些成绩细节 ... */ }
    void assert_valid() const {
        assert(score >= 0 && score <= 100);
        // ...
    }
};
```

其中需要注意的是, 在继承`Student`的同时, 也**继承了构造函数**。所以, 他们具有相同的内部布局、构造方式及接口, 从而实现了:

- 保证了, 使用上的一致性和间接测试的有效性
- 不修改源码, 做了测试相关功能的扩展, 更方便代码的测试
- 相对外部为其编写测试函数, 能访问到被保护的数据成员(一般建议以只读方式访问)

其实, 对于很多 "不改变类数据结构的前提下, 来扩展只读行为或工具函数的很多场景", **继承构造函数**都用发挥其作用

### 泛型装饰器和行为约束

**继承构造函数**不仅可以用于普通的继承中, 他还可以用于模板类型。例如, 下面定义的`NoCopy`中, 使用了`using T::T`对泛型T中的构造函数做继承。他的作用是在不改变目标对象的内存布局和使用接口下, 做一定的行为约束

```cpp
template <typename T>
class NoCopy : public T {
public:
    using T::T;

    NoCopy(const NoCopy&) = delete;
    NoCopy& operator=(const NoCopy&) = delete;
};
```

在一些模块或场景中, 我们期望再对象创想创建后, 不能再复制的方式创建其他对象时, 就可以在定义时使用这个`NoCopy`装饰器/包装器, 通过包装器中的`delete`显示告诉编译器删除了**拷贝构造**和**拷贝赋值**, 也意味着对象不在拥有**拷贝语义**。例如:

```cpp
class Point {
    double mX, mX;
public:
    Point() : mX { 0 }, mY { 0 } { }
    Point(double x, double y) : mX { x }, mY { y } { }

    string to_string() const {
        return "{ " + std::to_string(mX)
            + ", " + std::to_string(mY) + " }";
    }
};

Point p1(1, 2);
NoCopy<Point> p2(2, 3);

```

这个时候`p1`和`p2`在接口的使用上都是一样的, 但是`p2`相对`p1`就少了可拷贝的属性

```cpp
p1.to_string(); // ok
p2.to_string(); // ok

auto p3 = p1; // ok (拷贝构造)
auto p4 = p2; // error (不能拷贝)
```

## 二、注意事项

### 优先考虑继承还是组合

由于本章是介绍**继承构造函数**的特性和使用方式, 它是和**继承**性质绑定的。所以, 从实现上是倾向用继承的方式来实现的。 但是从于目标功能上考虑, 往往使用继承和组合都是可以实现的, 他们更偏向是手段而不是目的, 所以选择需要结合具体的应用场景。

例如, 对于一些测试环境, 或**仅功能函数扩展, 无数据结构变动**的场景下, 使用继承配合**继承构造函数**是比较方便的, 还可以避免大量的函数转发。但是, 对于一些 要对少量特定接口做"拦截"或较复杂的场景, 现在(2025)主流是更倾向用组合代替继承的

- 复杂场景或要加一个中间层做特殊处理 -> 一般组合优于继承
- 简单功能扩展, 且需保留接口使用的一致 -> 一般继承优于组合

## 三、其他

- [交流讨论](https://forum.d2learn.org/category/20)
- [mcpp-standard教程仓库](https://github.com/Sunrisepeak/mcpp-standard)
- [教程视频列表](https://space.bilibili.com/65858958/lists/5208246)
- [教程支持工具-xlings](https://github.com/d2learn/xlings)