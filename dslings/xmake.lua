add_includedirs(".")

-- 设置编码格式为 utf-8 修复emoji表情错误
set_encodings("source:utf-8", "target:utf-8")

target("00-0-hello-mcpp")
    if is_host("windows") then
        add_cxxflags("/W4 ", {force = true})  -- MSVC 不支持-Wpedantic -Werror，修改为 /W4 /WX
        -- add_cxxflags("/WX", {force = true})  --严格模式？（笑）
        set_languages("c++14")
    else
        add_cxxflags("-Wpedantic", {force = true})  -- GCC/Clang flags
        -- add_cxxflags("-Werror", {force = true})  -- 严格模式？（笑）
        set_languages("c++11")
    end
    add_files("hello-mcpp.cpp")

includes("CPP11")
