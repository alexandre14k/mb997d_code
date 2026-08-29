import sys
import root


def build_menu():
    print("m>app")
    print("r -- target release")
    print("g -- target debug")
    print("c -- target clean")
    print("m -- show the menu")
    print("x -- exit")


def build_release():
    return root.root_run_xmake_build(
        root.release_dir(), "release"
    )


def build_debug():
    return root.root_run_xmake_build(
        root.debug_dir(), "debug"
    )


def build_clean():
    return root.root_run_rmdir(root.target_dir())


def build_dispatch(cmd):
    if cmd == "r":
        build_release()
    elif cmd == "g":
        build_debug()
    elif cmd == "c":
        build_clean()
    elif cmd == "m":
        build_menu()
    elif cmd == "x":
        sys.exit(0)
    else:
        pass


def build_loop():
    build_menu()
    while True:
        cmd = input("build> ").strip()
        build_dispatch(cmd)


if __name__ == "__main__":
    build_loop()