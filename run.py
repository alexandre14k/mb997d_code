import os
import sys
import subprocess


def run_script_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "script"
    )


def run_ext_dir():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "ext"
    )


def run_menu():
    print("b -- manage build")
    print("d -- manage board")
    print("s -- manage ext")
    print("m -- show the menu")
    print("x -- exit")


def run_exec_build():
    path = os.path.join(run_script_dir(), "build.py")
    process = subprocess.run(
        [sys.executable, "-B", path],
        cwd=run_script_dir()
    )
    return process.returncode


def run_exec_board():
    path = os.path.join(run_script_dir(), "board.py")
    process = subprocess.run(
        [sys.executable, "-B", path],
        cwd=run_script_dir()
    )
    return process.returncode


def run_exec_ext():
    path = os.path.join(run_ext_dir(), "ext.py")
    process = subprocess.run(
        [sys.executable, "-B", path],
        cwd=run_ext_dir()
    )
    return process.returncode


def run_dispatch(cmd):
    if cmd == "b":
        run_exec_build()
    elif cmd == "d":
        run_exec_board()
    elif cmd == "s":
        run_exec_ext()
    elif cmd == "m":
        run_menu()
    elif cmd == "x":
        sys.exit(0)
    else:
        pass


def run_loop():
    run_menu()
    while True:
        cmd = input("run> ").strip()
        run_dispatch(cmd)


if __name__ == "__main__":
    run_loop()