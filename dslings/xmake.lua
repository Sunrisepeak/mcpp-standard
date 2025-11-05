if is_host("windows") then
    set_encodings("source:utf-8", "target:utf-8")
    set_toolchains("gcc")
    add_ldflags("-static")
end

if d2x.private.mcpp.lang == "zh" then
    add_includedirs(".")

    target("00-0-hello-mcpp")
        set_languages("cxx11")
        add_files("hello-mcpp.cpp")

    includes("cpp11")
else
    includes("en")
end
