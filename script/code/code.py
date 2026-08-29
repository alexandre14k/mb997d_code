import os

import base
import client
import root
import server


def code_menu():
    base.base_menu_print(
        "m>board>debug>code",
        [
            ("h", "help"),
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
            ("br <label>", "break"),
            ("c", "continue"),
            ("s", "step in"),
            ("n", "next"),
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
    if len(args) != 1:
        print("usage: br <label>")
        return 0

    return client.client_send(
        "break " + args[0]
    )


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

    if command == "c":
        return code_continue(args)

    if command == "s":
        return code_step(args)

    if command == "n":
        return code_next(args)

    if command == "h":
        return code_show_help(args)

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