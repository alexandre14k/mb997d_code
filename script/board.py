import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "code",
    ),
)

import base
import code
import root


def board_exec(name):
    path = os.path.join(root.root_dir(), name)
    return root.root_run(
        [sys.executable, "-B", path],
        root.root_dir(),
    )


def board_flash():
    return board_exec("flash.py")


def board_debug_erase(args):
    return board_exec("erase.py")


def board_debug_flash(args):
    return board_exec("flash.py")


def board_debug_reset(args):
    return board_exec("reset.py")


def board_debug_code(args):
    return code.code_main()


def board_menu():
    base.base_menu_print(
        "m>board",
        [
            ("f", "flash"),
            ("d", "debug"),
            ("m", "show the menu"),
            ("x", "exit"),
        ],
    )


def board_debug_menu():
    base.base_menu_print(
        "m>board>debug",
        [
            ("e", "erase"),
            ("f", "flash"),
            ("r", "reset"),
            ("c", "code"),
            ("m", "show the menu"),
            ("x", "exit"),
        ],
    )


def board_debug_help():
    base.base_help_print(
        "m>board>debug",
        [
            ("e", "erase"),
            ("f", "flash"),
            ("r", "reset"),
            ("c", "code"),
            ("h", "help"),
            ("m", "show the menu"),
            ("x", "exit"),
        ],
    )


def board_debug():
    handlers = {
        "e": board_debug_erase,
        "f": board_debug_flash,
        "r": board_debug_reset,
        "c": board_debug_code,
    }

    board_debug_menu()

    while True:
        line = input("debug> ").strip()
        parts = base.base_command_split(line)

        if not parts:
            continue

        command = parts[0]
        args = parts[1:]

        if command == "x":
            return 0

        if command == "h":
            board_debug_help()
            continue

        if command == "m":
            board_debug_menu()
            continue

        handler = handlers.get(command)

        if handler is None:
            continue

        result = handler(args)

        if result is not None and result != 0:
            return result


def board_dispatch(command):
    if command == "f":
        return board_flash()

    if command == "d":
        return board_debug()

    if command == "m":
        board_menu()
        return 0

    if command == "x":
        return 1

    return 0


def board_loop():
    board_menu()

    while True:
        line = input("board> ").strip()
        command = base.base_command_key(line)

        if not command:
            continue

        result = board_dispatch(command)

        if result == 1:
            return 0


if __name__ == "__main__":
    board_loop()
