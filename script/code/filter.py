def filter_openocd_message(line):
    line = line.rstrip()

    if not line:
        return None

    hidden = [
        "Open On-Chip Debugger",
        "Licensed under GNU GPL",
        "For bug reports",
        "http://openocd.org",
        "Info : auto-selecting",
        "Info : The selected transport",
        "Info : Listening on port",
        "Info : clock speed",
        "Info : STLINK",
        "Info : Target voltage",
        "Info : [stm32f4x.cpu] Cortex-M4",
        "Info : [stm32f4x.cpu] target has",
        "Info : starting gdb server",
        "Info : accepting 'gdb' connection",
        "Info : device id",
        "Info : flash size",
        "Info : Unable to match requested speed",
        "Unable to match requested speed",
        "halted: PC:",
        "[stm32f4x.cpu] halted",
        "xPSR:",
        "dropped 'gdb' connection",
        "shutdown command invoked",
    ]

    for text in hidden:
        if text in line:
            return None

    return line


def filter_gdb_message(line):
    line = line.rstrip()

    if not line:
        return None

    if line.startswith("(gdb) "):
        line = line[6:]

    if line == "(gdb)":
        return None

    hidden = [
        "GNU gdb ",
        "Copyright (C)",
        "License GPL",
        "This is free software",
        "There is NO WARRANTY",
        "Type \"show copying\"",
        "Type \"show configuration\"",
        "For bug reporting instructions",
        "Find the GDB manual",
        "For help, type",
        "Type \"apropos word\"",
        "This GDB was configured as",
        "http://www.gnu.org/software/gdb/documentation/",
        "https://www.gnu.org/software/gdb/",
        "Reading symbols from",
        "Detaching from program:",
        "Unable to match requested speed",
        "halted: PC:",
        "[stm32f4x.cpu] halted",
        "xPSR:",
    ]

    for text in hidden:
        if text in line:
            return None

    return line