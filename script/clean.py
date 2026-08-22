import root


def clean_main():
    code = root.root_run_rmdir(root.target_dir())
    root.root_fail(code)


if __name__ == "__main__":
    clean_main()