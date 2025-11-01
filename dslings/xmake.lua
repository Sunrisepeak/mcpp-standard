local dslings_dir = os.scriptdir()

includes(path.join(dslings_dir, "d2x/common.lua"))

if is_host("windows") then
    set_encodings("source:utf-8", "target:utf-8")
end

if get_local_lang() == "zh" then
    add_includedirs(".")

    target("00-0-hello-mcpp")
        set_languages("cxx11")
        add_files("hello-mcpp.cpp")

    includes("cpp11")
else
    includes("en")
end
