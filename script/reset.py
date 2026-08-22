import root


def reset_main():
    args = root.openocd_base_args() + [
        "-c", "init",
        "-c", "reset run",
        "-c", "exit",
    ]
    code = root.root_run_openocd(args)
    root.root_fail(code)


if __name__ == "__main__":
    reset_main()