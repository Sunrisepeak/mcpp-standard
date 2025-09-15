import sys, os
from manim import *

"""
Manim Community v0.18.1
manim -pql videos/cpp11/11-inherited-constructors.py
manim -pqh videos/cpp11/11-inherited-constructors.py
"""

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from d2x import *

class InheritedConstructors(MovingCameraScene):
    def construct(self):

        title, logo = mcpp_video_start(self, "{ 继承构造函数 }")

        self.wait(0.5)

        jicheng_text = Text("继承", t2c = { '继承': RED })
        jicheng_text.scale(3)
        jicheng_text.set_opacity(0.1)

        self.play(ReplacementTransform(title[1:3].copy(), jicheng_text))
        self.bring_to_back(jicheng_text)

        self.wait(0.5)

        # 1: 构造逻辑复用
        self.play(
            FadeOut(jicheng_text),
            Transform(title, Text("{ 1 - 复用基类构造函数 }", t2c = { '复用': RED }))
        )

        code_1_1 = self.create_code_helper("""
class ObjectBase {
public:
    ObjectBase(int) {}
    ObjectBase(double) {}
    // 其他实现
};

class MyObject : public ObjectBase {
public:
    MyObject(int x) : ObjectBase(x) {}
    MyObject(double y) : ObjectBase(y) {}
    // 其他实现
};
""")

        code_1_1.code[4].set_color(PURE_RED)
        code_1_1.code[11].set_color(PURE_RED)

        self.wait(0.5)
        self.play(ReplacementTransform(title, code_1_1))

        self.wait(0.5)
        self.play(
            DHighlight(code_1_1.code[9][22:36]),
            DHighlight(code_1_1.code[10][25:39])
        )

        question = Text("?").scale(3)
        question.set_color(RED)
        question.set_opacity(0.2)
        question.move_to(UR * 1.5 + RIGHT)

        self.wait(0.5)
        self.play(Write(question))

        code_1_1_from_9_to_11 = VGroup(
            code_1_1.code[9],
            code_1_1.code[10],
            code_1_1.code[11],
        )
        code_1_1_from_9_to_11_copy = code_1_1_from_9_to_11.copy()

        using_objectbase = Text("using ObjectBase::ObjectBase;")
        using_objectbase.scale(0.5)
        using_objectbase.set_color(PURE_RED)
        using_objectbase.next_to(code_1_1.code[8], DOWN, aligned_edge=LEFT)
        using_objectbase.shift(RIGHT)

        self.wait(0.5)
        #code_1_1_from_9_to_11.set_opacity(0)
        self.play(
            FadeOut(question),
            ReplacementTransform(code_1_1_from_9_to_11, using_objectbase)
        )

        self.wait(0.5)

        self.play(
            FadeIn(code_1_1_from_9_to_11_copy, shift=UP),
            FadeOut(using_objectbase, shift=DOWN)
        )

        self.play(
            FadeOut(code_1_1_from_9_to_11_copy, shift=DOWN),
            FadeIn(using_objectbase, shift=UP)
        )


        # 2: 类型的功能扩展
        self.wait(0.5)
        title = Text("{ 2 - 类型的功能扩展 }", t2c = { '功能扩展': RED })
        code_1_1.set_opacity(0.5)
        self.play(
            FadeOut(code_1_1),
            Transform(using_objectbase, title)
        )

        code_2_1 = self.create_code_helper("""class ObjectXXX : public Object {
public:
    using Object::Object;

    void your_method() { /* ... */ }
};
""")

        self.wait(0.5)
        self.play(ReplacementTransform(using_objectbase, code_2_1))

        self.wait(0.5)
        self.play(DHighlight(code_2_1.code[4]))

        code_2_2 = self.create_code_helper("""class Student {
protected:
    double score;
public:
    string id;
    string name;
    uint age;

    Student(string id, string name);
    Student(string id, string name, uint age);
    Student(string id, ...);
};""")
        
        self.wait(0.5)
        self.play(ReplacementTransform(code_2_1, code_2_2))

        for i in [8, 9, 10]:
            self.play(DHighlight(code_2_2.code[i]), run_time=0.5)

        code_2_3 = self.create_code_helper("""class StudentDebug : public Student {
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
};""")
        
        self.wait(0.5)
        self.play(
            FadeOut(code_2_2),
            FadeIn(code_2_3, shift=LEFT * 2),
        )

        select_box = SurroundingRectangle(code_2_3.code[4:8], color=PURE_RED)
        select_box.shift(DOWN * 0.3)
        self.wait(0.5)
        self.play(Create(select_box))

        code_2_4 = self.create_code_helper("""Student s1("2024001", "Alice");
StudentDebug s2("2024002", "Bob", 20);
s1.set_score(22);
s2.set_score(33);
s1.to_string(); // error (没有 to_string 方法)
s2.to_string(); // ok""")
        
        code_2_4.scale(0.75)
        code_2_4.shift(RIGHT * 2.5 + DOWN * 1)
        code_2_4.code[4].set_color(PURE_RED)
        code_2_4.code[5].set_color(PURE_GREEN)

        self.wait(0.5)
        self.play(
            code_2_3.animate.set_opacity(0.5),
            Transform(select_box, code_2_4)
        )

        # 3: 异常或错误类型标识和转发
        self.wait(0.5)
        title = Text("{ 3 - 异常或错误类型标识和转发 }", t2c = { '类型标识': RED })
        self.play(
            FadeOut(code_2_3),
            ReplacementTransform(select_box, title)
        )

        code_3_1 = self.create_code_helper("""class ErrorBase {
public:
    ErrorBase() { }
    ErrorBase(const char *) { }
    ErrorBase(std::string) { }
    //...
};""")
        code_3_1.code[5].set_color(PURE_RED)

        self.wait(0.5)
        self.play(ReplacementTransform(title, code_3_1))

        config_error = Text("配置错误").scale(0.7)
        config_error.shift(UL * 1.5 + LEFT).set_color(RED)
        runtime_error = Text("运行时错误").scale(0.7)
        runtime_error.shift(UR * 1.5 + RIGHT).set_color(GREEN)
        io_error = Text("IO错误").scale(0.7)
        io_error.shift(DOWN).set_color(BLUE)

        self.play(FadeOut(code_3_1), FadeIn(config_error, shift=UL * 1.5), run_time = 0.5)
        self.play(FadeIn(runtime_error, shift=UR * 1.5), run_time = 0.5)
        self.play(FadeIn(io_error, shift=DOWN), run_time = 0.5)

        code_3_2 = self.create_code_helper("""class ConfigError : public ErrorBase {
public:
    using ErrorBase::ErrorBase;
};

class RuntimeError : public ErrorBase {
public:
    using ErrorBase::ErrorBase;
};

class IoError : public ErrorBase {
public:
    using ErrorBase::ErrorBase;
};""")
        
        self.wait(0.5)
        error_group = VGroup(config_error, runtime_error, io_error)
        self.play(ReplacementTransform(error_group, code_3_2))

        code_3_3 = self.create_code_helper("""struct MyErrProcessor {
    static void process(ErrorBase err) { 基础处理 }
    static void process(ConfigError err) { 配置错误处理 }
};

MyErrProcessor::process(errObj); // 自动匹配错误处理函数
""")

        code_3_3.code[5].set_color(YELLOW)

        self.wait(0.5)
        self.play(ReplacementTransform(code_3_2, code_3_3))

        # 4: 泛型装饰器和行为约束
        self.wait(0.5)
        title = Text("{ 4 - 泛型装饰器和行为约束 }", t2c = { '泛型装饰器': RED })
        self.play(ReplacementTransform(code_3_3, title))

        code_4_1 = self.create_code_helper("""template <typename T>
class NoCopy : public T {
public:
    using T::T;

    NoCopy(const NoCopy&) = delete;
    NoCopy& operator=(const NoCopy&) = delete;
    // ...
};""")

        self.wait(0.5)
        self.play(ReplacementTransform(title, code_4_1))

        self.wait(0.5)
        select_box = SurroundingRectangle(code_4_1.code[3], color=PURE_RED)
        self.play(Create(select_box))

        select_box_tmp = SurroundingRectangle(code_4_1.code[4:7], color=PURE_RED)
        select_box_tmp.shift(DOWN * 0.3)
        self.wait(0.5)
        copy_semantics = Text("删除拷贝语义").scale(0.7).set_color(RED)
        copy_semantics.shift(RIGHT * 2.5 + UP)
        self.play(
            FadeIn(copy_semantics),
            Transform(select_box, select_box_tmp)
        )

        code_4_2 = self.create_code_helper("""class Point {
    double mX, mY;
public:
    Point() : mX { 0 }, mY { 0 } { }
    Point(double x, double y) : mX { x }, mY { y } { }

    string to_string() const {
        return "{ " + std::to_string(mX)
            + ", " + std::to_string(mY) + " }";
    }
};

Point p1(1, 2);
NoCopy<Point> p2(2, 3);""")
        
        code_4_3 = self.create_code_helper("""p1.to_string(); // ok
p2.to_string(); // ok

auto p3 = p1; // ok (拷贝构造)
auto p4 = p2; // error (不能拷贝)
""")

        code_4_3.scale(0.7)
        code_4_3.shift(DR * 2 + RIGHT * 0.35 + UP * 0.2)

        p2_code_line = VGroup(code_4_3.code[1], code_4_3.code[4]).copy()
        p2_code_line[0].set_color(PURE_GREEN)
        p2_code_line[1].set_color(PURE_RED)

        code_4_3.code[0].set_color(PURE_GREEN)
        code_4_3.code[3].set_color(PURE_GREEN)

        code_4_3.code[1].set_opacity(0)
        code_4_3.code[4].set_opacity(0)

        p2_object_code_line = code_4_2.code[13].copy()

        self.wait(0.5)
        self.play(
            FadeOut(copy_semantics),
            ReplacementTransform(select_box, code_4_3),
            ReplacementTransform(code_4_1, code_4_2)
        )

        self.wait(0.5)
        self.play(ReplacementTransform(p2_object_code_line, p2_code_line))

        # 5: 优先考虑继承还是组合
        self.wait(0.5)
        p2_code_line.set_opacity(0)
        title = Text("继承  ?  组合", t2c = { '继承': RED, '组合': YELLOW })

        title.scale(1.5)

        self.play(
            FadeOut(code_4_2, code_4_3),
            FadeIn(title)
        )

        self.wait(0.5)
        self.play(FadeOut(title))

        mcpp_video_end(self, logo)


    @staticmethod
    def create_code_helper(code: str):
        return Code(
            code=code,
            background="",
            language="cpp",
        )

if __name__ == "__main__":
    scene = InheritedConstructors()
    scene.render()