target("app")
    set_kind("binary")
    set_extension(".elf")
    add_files("main.c")
    add_files("src/*.c")
    add_deps("hal")
    add_ldflags(
        "-L" .. path.join(os.scriptdir(), "bsp"),
        {force = true}
    )
    add_ldflags(
        "-T" .. path.join(os.scriptdir(), "bsp/link.ld"),
        {force = true}
    )
    add_ldflags(
        "--specs=nosys.specs",
        {force = true}
    )
    add_ldflags(
        "-nostartfiles",
        {force = true}
    )
    after_link(function (target)
        local function app_tool(name)
            return "arm-none-eabi-" .. name
        end

        local function app_paths()
            local elf = target:targetfile()
            local dir = path.directory(elf)
            local name = path.basename(elf)
            return elf, path.join(dir, name .. ".hex"),
                path.join(dir, name .. ".bin")
        end

        local function app_gen_hex(elf, hex)
            os.execv(app_tool("objcopy"), {"-O", "ihex", elf, hex})
        end

        local function app_gen_bin(elf, bin)
            os.execv(app_tool("objcopy"), {"-O", "binary", elf, bin})
        end

        local function app_file_kb(path_str)
            local size = os.filesize(path_str)
            return string.format("%.2f", size / 1024)
        end

        local function app_size_line(elf)
            local outdata = os.iorunv(app_tool("size"), {elf})
            local lines = {}
            for line in outdata:gmatch("[^\n]+") do
                table.insert(lines, line)
            end
            return lines[2]
        end

        local function app_report_size(elf)
            local line = app_size_line(elf)
            local t, d, b = line:match("(%d+)%s+(%d+)%s+(%d+)")
            t = tonumber(t)
            d = tonumber(d)
            b = tonumber(b)
            print("flash used -- " .. (t + d) .. " bytes")
            print("ram used -- " .. (d + b) .. " bytes")
        end

        local function app_report_file_sizes(elf, hex, bin)
            print("elf size -- " .. app_file_kb(elf) .. " kb")
            print("hex size -- " .. app_file_kb(hex) .. " kb")
            print("bin size -- " .. app_file_kb(bin) .. " kb")
        end

        local function app_symbol_count(elf)
            local count = 0
            try
            {
                function ()
                    local outdata = os.iorunv(
                        app_tool("nm"), {elf}
                    )
                    for _ in outdata:gmatch("[^\n]+") do
                        count = count + 1
                    end
                end,
                catch
                {
                    function (errors)
                    end
                }
            }
            return count
        end

        local function app_strip(elf)
            os.execv(app_tool("strip"), {"--strip-all", elf})
        end

        local elf, hex, bin = app_paths()
        app_gen_hex(elf, hex)
        app_gen_bin(elf, bin)
        app_report_size(elf)
        app_report_file_sizes(elf, hex, bin)

        local function app_report_result(elf, hex, bin, dbg_mode)
            local symbols = app_symbol_count(elf)
            print("symbols -- " .. symbols)
            print("elf -- " .. elf)
            print("hex -- " .. hex)
            print("bin -- " .. bin)
            print("flash with openocd -- " .. elf)
            if dbg_mode then
                print("debug with openocd -- " .. elf)
            end
            print("load with bootloader -- " .. bin)
        end

        if is_mode("debug") then
            app_report_result(elf, hex, bin, true)
            return
        else
            app_strip(elf)
            app_report_result(elf, hex, bin, false)
        end

    end)