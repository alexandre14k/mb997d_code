import os

import base
import client
import root
import server


def code_menu():
    base.base_menu_print(
        "m>board>debug>code",
        [
            ("at", "attach"),
            ("re", "reinit"),
            ("br <label>", "set break point"),
            ("d", "delete all break points"),
            ("c", "continue"),
            ("ls", "preview next lines"),
            ("s", "step in"),
            ("o", "step out"),
            ("n", "next"),
            ("", ""),
            ("h", "tell me more"),
            ("m", "show the menu"),
            ("x", "exit"),
        ],
    )


def code_help():
    base.base_help_print(
        "code",
        [
            ("at", "attach"),
            ("re", "reinit"),
            ("br <label>", "set break point"),
            ("d", "delete all break points"),
            ("c", "continue"),
            ("ls", "preview next lines"),
            ("s", "step in"),
            ("o", "step out"),
            ("n", "next"),
            ("ch <expression>", "get as char"),
            ("str <expression>", "get as str"),
            ("bin <expression>", "get as bin"),
            ("hex <expression>", "get as hex"),
            ("get addr <expression>", "get as hex address"),
            ("set char <expression>", "allocate and set char"),
            ("set short <expression>", "allocate and set short"),
            ("set int <expression>", "allocate and set int"),
            ("set uchar <expression>", "allocate and set unsigned char"),
            ("set ushort <expression>", "allocate and set unsigned short"),
            ("set uint <expression>", "allocate and set unsigned int"),
            ("m", "show the menu"),
            ("x", "exit"),
        ],
    )


def code_debug_elf_exists():
    return os.path.isfile(
        root.app_elf_path("debug")
    )


def code_recover():
    client.client_stop()
    server.server_stop()

    if server.server_start() != 0:
        return 1

    if client.client_start() != 0:
        server.server_stop()
        return 1

    return 0


def code_attach(args):
    if client.client_connected():
        if client.client_responsive():
            return 0

        code = code_recover()

        if code != 0:
            return code

        return client.client_send(
            "target extended-remote localhost:3333"
        )

    code = client.client_send(
        "target extended-remote localhost:3333"
    )

    if code == 0:
        return 0

    code = code_recover()

    if code != 0:
        return code

    return client.client_send(
        "target extended-remote localhost:3333"
    )


def code_reinit(args):
    if not client.client_connected():
        code = client.client_send(
            "target extended-remote localhost:3333"
        )

        if code != 0:
            return code

    return client.client_send(
        "monitor reset halt"
    )


def code_break(args):
    expression = code_expression(args, "br")

    if expression is None:
        return 0

    return client.client_send(
        "break " + expression
    )

def code_delete_breaks(args):
    if args:
        print("usage: d")
        return 0

    return client.client_send(
        "delete breakpoints"
    )


def code_step_out(args):
    if args:
        print("usage: o")
        return 0

    return client.client_send(
        "finish"
    )


def code_expression(args, command_name):
    if not args:
        print("usage: " + command_name + " <expression>")
        return None
    return " ".join(args)


def code_get_address(args):
    expression = code_expression(args, "get addr")

    if expression is None:
        return 0

    return client.client_send(
        "p/x &(" + expression + ")"
    )


def code_set_value(args, type_name, command_name):
    if len(args) < 1:
        print("usage: " + command_name + " <expression>")
        return 0

    expression = " ".join(args)

    sizes = {
        "char": "sizeof(char)",
        "short": "sizeof(short)",
        "int": "sizeof(int)",
        "uchar": "sizeof(unsigned char)",
        "ushort": "sizeof(unsigned short)",
        "uint": "sizeof(unsigned int)",
    }

    gdb_types = {
        "char": "char",
        "short": "short",
        "int": "int",
        "uchar": "unsigned char",
        "ushort": "unsigned short",
        "uint": "unsigned int",
    }

    size = sizes[type_name]
    gdb_type = gdb_types[type_name]

    commands = [
        "set $code_memory = (" + gdb_type + " *) malloc(" + size + ")",
        "set {" + gdb_type + "} $code_memory = " + expression,
        "p/x $code_memory",
    ]

    for command in commands:
        code = client.client_send(command)

        if code != 0:
            return code

    return 0


def code_print_value(args, format_specifier, command_name):
    expression = code_expression(args, command_name)

    if expression is None:
        return 0

    return client.client_send(
        "p/" + format_specifier + " " + expression
    )

def code_print_char(args):
    return code_print_value(args, "c", "ch")


def code_print_string(args):
    return code_print_value(args, "s", "str")


def code_print_binary(args):
    return code_print_value(args, "t", "bin")


def code_print_hex(args):
    return code_print_value(args, "x", "hex")


def code_set_char(args):
    return code_set_value(args, "char", "set char")


def code_set_short(args):
    return code_set_value(args, "short", "set short")


def code_set_int(args):
    return code_set_value(args, "int", "set int")


def code_set_uchar(args):
    return code_set_value(args, "uchar", "set uchar")


def code_set_ushort(args):
    return code_set_value(args, "ushort", "set ushort")


def code_set_uint(args):
    return code_set_value(args, "uint", "set uint")


def code_ls(args):
    if args:
        print("usage: ls")
        return 0

    script = (
        "import gdb;"
        "f=gdb.newest_frame();"
        "s=f.find_sal();"
        "p=s.symtab.fullname();"
        "l=s.line;"
        "x=open(p).read().splitlines();"
        "e=min(len(x),l+19);"
        "print('...');"
        "print('\\n'.join([str(i)+'\\t'+x[i-1] for i in range(l,e+1)]));"
        "print('...')"
    )

    return client.client_send("python " + script)


def code_continue(args):
    return client.client_send(
        "continue"
    )


def code_step(args):
    return client.client_send(
        "step"
    )


def code_next(args):
    return client.client_send(
        "next"
    )


def code_show_help(args):
    code_help()
    return 0


def code_show_menu(args):
    code_menu()
    return 0


def code_dispatch(command, args):
    if command == "at":
        return code_attach(args)

    if command == "re":
        return code_reinit(args)

    if command == "br":
        return code_break(args)

    if command == "d":
        return code_delete_breaks(args)

    if command == "c":
        return code_continue(args)

    if command == "ls":
        return code_ls(args)

    if command == "s":
        return code_step(args)

    if command == "o":
        return code_step_out(args)

    if command == "n":
        return code_next(args)

    if command == "ch":
        return code_print_char(args)

    if command == "str":
        return code_print_string(args)

    if command == "bin":
        return code_print_binary(args)

    if command == "hex":
        return code_print_hex(args)

    if command == "h":
        return code_show_help(args)

    if command == "get" and len(args) >= 2 and args[0] == "addr":
        return code_get_address(args[1:])

    if command == "set" and len(args) >= 2:
        if args[0] == "char":
            return code_set_char(args[1:])
        if args[0] == "short":
            return code_set_short(args[1:])
        if args[0] == "int":
            return code_set_int(args[1:])
        if args[0] == "uchar":
            return code_set_uchar(args[1:])
        if args[0] == "ushort":
            return code_set_ushort(args[1:])
        if args[0] == "uint":
            return code_set_uint(args[1:])

    if command == "m":
        return code_show_menu(args)

    if command == "x":
        return 1

    print("unknown command: " + command)
    return 0


def code_session():
    if not code_debug_elf_exists():
        print("setup app with debug build first")
        return 1

    if server.server_start() != 0:
        return 1

    if client.client_start() != 0:
        server.server_stop()
        return 1

    try:
        code_menu()

        while True:
            line = input("code> ").strip()
            parts = base.base_command_split(line)

            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            result = code_dispatch(
                command,
                args,
            )

            if result == 1:
                return 0

    finally:
        client.client_stop()
        server.server_stop()


def code_main():
    return code_session()


if __name__ == "__main__":
    code_main()