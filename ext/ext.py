import os
import sys
import subprocess
import shutil
import re


def ext_dir():
    return os.path.dirname(os.path.abspath(__file__))


def ext_items():
    return [
        (
            "stm32", "hal",
            "https://github.com/STMicroelectronics/"
            "stm32f4xx-hal-driver",
            None
        ),
        (
            "stm32", "cmsis_device",
            "https://github.com/STMicroelectronics/"
            "cmsis_device_f4",
            None
        ),
        (
            "stm32", "cmsis_core",
            "https://github.com/ARM-software/CMSIS_5",
            ["CMSIS/Core/Include"]
        ),
    ]


def ext_item_dir(group, name):
    return os.path.join(ext_dir(), group, name)


def ext_item_relpath(group, name):
    return os.path.relpath(
        ext_item_dir(group, name),
        os.path.dirname(ext_dir())
    )


def ext_clone_relpath(path):
    return os.path.relpath(path, ext_dir())


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


def ext_hal_url():
    for group, name, url, _ in ext_items():
        if group == "stm32" and name == "hal":
            return url
    return ""


def ext_arch():
    match = re.search(r"stm32(\w+)-hal-driver", ext_hal_url())
    if match:
        return match.group(1)
    return "unknown"


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


def ext_update_one(group, name, url, paths):
    path = ext_item_dir(group, name)
    print('path is "' + ext_item_relpath(group, name) + '"')
    if os.path.isdir(path) and ext_has_origin(path):
        ext_run(["git", "fetch", "origin"], path)
        branch = ext_default_branch(path)
        return ext_run(
            ["git", "reset", "--hard", "origin/" + branch],
            path
        )
    if paths:
        return ext_clone_sparse(url, path, paths)
    return ext_clone_full(url, path)


def ext_update():
    code = 0
    for group, name, url, paths in ext_items():
        result = ext_update_one(group, name, url, paths)
        if result != 0:
            code = result
    return code


def ext_archive_prefix(group, name):
    return "stm32_" + ext_arch() + "_" + name


def ext_archive_one(group, name):
    path = ext_item_dir(group, name)
    if not os.path.isdir(path):
        print(name + " not cloned, skip")
        return 0
    base = (
        ext_archive_prefix(group, name) +
        "_" + ext_commit_short(path)
    )
    dest = os.path.join(ext_dir(), base)
    zip_path = dest + ".zip"
    if os.path.isfile(zip_path):
        os.remove(zip_path)
    shutil.make_archive(dest, "zip", path)
    print("archived -- " + base + ".zip")
    return 0


def ext_archive():
    code = 0
    for group, name, _, _ in ext_items():
        result = ext_archive_one(group, name)
        if result != 0:
            code = result
    return code


def ext_confirm(prompt):
    answer = input(prompt + " [y/N] ").strip().lower()
    return answer == "y"


def ext_remove_one(group, name):
    path = ext_item_dir(group, name)
    if not os.path.isdir(path):
        return 0
    if sys.platform.startswith("win"):
        return ext_run(["rmdir", "/s", "/q", path])
    return ext_run(["rm", "-rf", path])


def ext_clean():
    present = [
        (group, name) for group, name, _, _ in ext_items()
        if os.path.isdir(ext_item_dir(group, name))
    ]
    if not present:
        return 0
    labels = [name for _, name in present]
    if not ext_confirm("remove " + ", ".join(labels) + " ?"):
        return 1
    code = 0
    for group, name in present:
        result = ext_remove_one(group, name)
        if result != 0:
            code = result
    return code


def ext_menu():
    print("# arch " + ext_arch())
    print("u -- update ext folder")
    print("c -- clean ext folder")
    print("a -- archive ext folder")
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