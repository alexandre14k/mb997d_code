import os
import sys
import subprocess
import root


def board_exec(name):
    path = os.path.join(root.root_dir(), name)
    process = subprocess.run(
        [sys.executable, "-B", path],
        cwd=root.root_dir()
    )
    return process.returncode


def board_exec_arg(name, arg):
    path = os.path.join(root.root_dir(), name)
    process = subprocess.run(
        [sys.executable, "-B", path, arg],
        cwd=root.root_dir()
    )
    return process.returncode


def board_trace_hints():
    path = os.path.join(root.root_dir(), "trace.rst")
    with open(path) as handle:
        print(handle.read())


def board_menu():
    print("e -- erase")
    print("f -- flash")
    print("r -- reset")
    print("d -- start debugger")
    print("t -- trace debugger")
    print("h -- trace hints")
    print("q -- force debugger stop")
    print("m -- show the menu")
    print("x -- exit")


def board_dispatch(cmd):
    if cmd == "e":
        board_exec("erase.py")
    elif cmd == "f":
        board_exec("flash.py")
    elif cmd == "r":
        board_exec("reset.py")
    elif cmd == "d":
        board_exec_arg("trace.py", "d")
    elif cmd == "t":
        board_exec_arg("trace.py", "t")
    elif cmd == "h":
        board_trace_hints()
    elif cmd == "q":
        board_exec_arg("trace.py", "q")
    elif cmd == "m":
        board_menu()
    elif cmd == "x":
        sys.exit(0)
    else:
        pass


def board_loop():
    board_menu()
    while True:
        cmd = input("board> ").strip()
        board_dispatch(cmd)


if __name__ == "__main__":
    board_loop()