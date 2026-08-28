set_project("app")

set_targetdir("$(builddir)")
add_rules("mode.debug", "mode.release")

if is_mode("release") then
    set_optimize("smallest")
end

toolchain("arm-none-eabi")
    set_kind("standalone")
    set_toolset("cc", "arm-none-eabi-gcc")
    set_toolset("as", "arm-none-eabi-gcc")
    set_toolset("ld", "arm-none-eabi-gcc")
    set_toolset("ar", "arm-none-eabi-ar")
    set_toolset("objcopy", "arm-none-eabi-objcopy")
    set_toolset("strip", "arm-none-eabi-strip")
    on_check(function (toolchain)
        return true
    end)
toolchain_end()

set_toolchains("arm-none-eabi")

set_arch("cortex-m4")

add_defines("STM32F407xx")

add_cflags(
    "-mcpu=cortex-m4",
    "-mthumb",
    "-mfloat-abi=softfp",
    "-mfpu=fpv4-sp-d16",
    {force = true}
)

add_ldflags(
    "-mcpu=cortex-m4",
    "-mthumb",
    "-mfloat-abi=softfp",
    "-mfpu=fpv4-sp-d16",
    {force = true}
)

add_includedirs("../app/bsp")

includes("../ext/xmake.lua")
includes("../app/xmake.lua")