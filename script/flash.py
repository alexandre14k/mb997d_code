import root


def flash_prompt_mode():
    answer = input("flash release or debug ? [r/d] ").strip().lower()
    if answer == "d":
        return "debug"
    return "release"


def flash_main():
    mode = flash_prompt_mode()
    elf = root.app_elf_path(mode)
    args = root.openocd_base_args() + [
        "-c", "program " + elf + " verify reset exit",
    ]
    code = root.root_run_openocd(args)
    root.root_fail(code)


if __name__ == "__main__":
    flash_main()