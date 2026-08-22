import os
import sys
import subprocess
import shutil
import re


def ext_commit_short(path):
    process = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=path,
        capture_output=True,
        text=True
    )
    commit = process.stdout.strip()
    if not commit:
        return "unknown"
    return commit


def ext_archive_name(name, path):
    return (
        "stm32_" + ext_arch() + "_" + name +
        "_" + ext_commit_short(path)
    )

def ext_archive_one(name):
    path = ext_repo_dir(name)
    if not os.path.isdir(path):
        print(name + " not cloned, skip")
        return 0
    base = ext_archive_name(name, path)
    dest = os.path.join(ext_dir(), base)
    zip_path = dest + ".zip"
    if os.path.isfile(zip_path):
        os.remove(zip_path)
    shutil.make_archive(dest, "zip", path)
    print("archived -- " + base + ".zip")
    return 0


def ext_archive():
    code = 0
    for name, _ in ext_repos():
        result = ext_archive_one(name)
        if result != 0:
            code = result
    return code


def ext_dir():
    return os.path.dirname(os.path.abspath(__file__))


def ext_hal_url():
    for name, url in ext_repos():
        if name == "hal":
            return url
    return ""


def ext_arch():
    match = re.search(r"stm32(\w+)-hal-driver", ext_hal_url())
    if match:
        return match.group(1)
    return "unknown"


def ext_repos():
    return [
        (
            "hal",
            "https://github.com/STMicroelectronics/"
            "stm32f4xx-hal-driver"
        ),
        (
            "cmsis_device",
            "https://github.com/STMicroelectronics/"
            "cmsis_device_f4"
        ),
        (
            "cmsis_core",
            "https://github.com/ARM-software/CMSIS_5"
        ),
    ]

def ext_sparse_paths():
    return {
        "cmsis_core": ["CMSIS/Core/Include"],
    }


def ext_repo_dir(name):
    return os.path.join(ext_dir(), "stm32", name)


def ext_clone_relpath(path):
    return os.path.relpath(path, ext_dir())


def ext_relpath(name):
    return os.path.relpath(
        ext_repo_dir(name),
        os.path.dirname(ext_dir())
    )


def ext_run(cmd, cwd=None):
    process = subprocess.run(cmd, cwd=cwd if cwd else ext_dir())
    return process.returncode


def ext_has_origin(path):
    process = subprocess.run(
        ["git", "remote"],
        cwd=path,
        capture_output=True,
        text=True
    )
    return "origin" in process.stdout.split()


def ext_default_branch(path):
    process = subprocess.run(
        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
        cwd=path,
        capture_output=True,
        text=True
    )
    ref = process.stdout.strip()
    if not ref:
        return "master"
    return ref.rsplit("/", 1)[-1]


def ext_clone_sparse(url, path, paths):
    code = ext_run([
        "git", "clone",
        "--filter=blob:none",
        "--sparse",
        "--depth", "1",
        url, ext_clone_relpath(path)
    ])
    if code != 0:
        return code
    code = ext_run(
        ["git", "sparse-checkout", "init", "--cone"],
        path
    )
    if code != 0:
        return code
    return ext_run(
        ["git", "sparse-checkout", "set"] + paths,
        path
    )


def ext_clone_full(url, path):
    return ext_run(["git", "clone", url, ext_clone_relpath(path)])


def ext_update_one(name, url):
    path = ext_repo_dir(name)
    print('path is "' + ext_relpath(name) + '"')
    if os.path.isdir(path) and ext_has_origin(path):
        ext_run(["git", "fetch", "origin"], path)
        branch = ext_default_branch(path)
        return ext_run(
            ["git", "reset", "--hard", "origin/" + branch],
            path
        )
    paths = ext_sparse_paths().get(name)
    if paths:
        return ext_clone_sparse(url, path, paths)
    return ext_clone_full(url, path)


def ext_update():
    code = 0
    for name, url in ext_repos():
        result = ext_update_one(name, url)
        if result != 0:
            code = result
    return code


def ext_confirm(prompt):
    answer = input(prompt + " [y/N] ").strip().lower()
    return answer == "y"


def ext_remove_one(name):
    path = ext_repo_dir(name)
    if not os.path.isdir(path):
        return 0
    if sys.platform.startswith("win"):
        return ext_run(["rmdir", "/s", "/q", path])
    return ext_run(["rm", "-rf", path])


def ext_clean():
    names = [name for name, _ in ext_repos()
             if os.path.isdir(ext_repo_dir(name))]
    if not names:
        return 0
    if not ext_confirm("remove " + ", ".join(names) + " ?"):
        return 1
    code = 0
    for name in names:
        result = ext_remove_one(name)
        if result != 0:
            code = result
    return code


def ext_menu():
    print("# arch " + ext_arch())
    print("u -- update stm32 folder")
    print("c -- clean stm32 folder")
    print("a -- archive stm32 folder")
    print("m -- show the menu")
    print("x -- exit")


def ext_dispatch(cmd):
    if cmd == "u":
        ext_update()
    elif cmd == "c":
        ext_clean()
    elif cmd == "a":
        ext_archive()
    elif cmd == "m":
        ext_menu()
    elif cmd == "x":
        sys.exit(0)
    else:
        pass


def ext_loop():
    ext_menu()
    while True:
        cmd = input("ext> ").strip()
        ext_dispatch(cmd)


if __name__ == "__main__":
    ext_loop()