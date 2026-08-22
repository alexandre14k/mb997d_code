import root


def erase_main():
    args = root.openocd_base_args() + [
        "-c", "init",
        "-c", "reset init",
        "-c", "stm32f4x mass_erase 0",
        "-c", "exit",
    ]
    code = root.root_run_openocd(args)
    root.root_fail(code)


if __name__ == "__main__":
    erase_main()