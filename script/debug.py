import root


def debug_main():
    code = root.root_run_xmake_build(
        root.debug_dir(), "debug"
    )
    root.root_fail(code)


if __name__ == "__main__":
    debug_main()