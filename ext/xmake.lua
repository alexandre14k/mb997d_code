target("hal")
    set_kind("static")
    add_files("stm32/hal/Src/*.c")
    remove_files("stm32/hal/Src/*_template.c")
    add_files("stm32/cmsis_device/Source/Templates/system_stm32f4xx.c")
    add_files("stm32/cmsis_device/Source/Templates/gcc/startup_stm32f407xx.s")
    add_includedirs("stm32/hal/Inc", {public = true})
    add_includedirs(
        "stm32/hal/Inc/Legacy",
        {public = true}
    )
    add_includedirs(
        "stm32/cmsis_device/Include",
        {public = true}
    )
    add_includedirs(
        "stm32/cmsis_core/CMSIS/Core/Include",
        {public = true}
    )