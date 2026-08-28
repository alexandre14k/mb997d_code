import os
import sys
import subprocess
import platform
import signal

def root_child_default_sigint():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

def root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def base_dir():
    return os.path.dirname(root_dir())


def root_relpath(path):
    return os.path.relpath(path, root_dir())


def app_dir():
    return os.path.join(base_dir(), "app")


def ext_dir():
    return os.path.join(base_dir(), "ext")


def target_dir():
    return os.path.join(base_dir(), "target")


def release_dir():
    return os.path.join(target_dir(), "release")


def debug_dir():
    return os.path.join(target_dir(), "debug")


def root_platform():
    system = platform.system().lower()
    if system.startswith("win"):
        return "win32"
    if system.startswith("darwin"):
        return "macos"
    return "linux"


def root_env(name, default):
    return os.environ.get(name, default)


def toolchain_gcc():
    if root_platform() == "win32":
        return root_env("ROOT_GCC", "arm-none-eabi-gcc.exe")
    return root_env("ROOT_GCC", "arm-none-eabi-gcc")


def toolchain_xmake():
    if root_platform() == "win32":
        return root_env("ROOT_XMAKE", "xmake.exe")
    return root_env("ROOT_XMAKE", "xmake")


def toolchain_openocd():
    if root_platform() == "win32":
        return root_env("ROOT_OPENOCD", "openocd.exe")
    return root_env("ROOT_OPENOCD", "openocd")


def root_kill_process(pid):
    if not pid:
        if root_platform() == "win32":
            subprocess.run(["taskkill", "/IM", "openocd.exe", "/F"])
        else:
            subprocess.run(
                ["pkill", "-9", "-x", "openocd"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        return

    if root_platform() == "win32":
        subprocess.run(["taskkill", "/PID", str(pid), "/F"])
        return
    try:
        os.kill(pid, 9)
    except OSError:
        pass


def root_remove_pid(path):
    if os.path.isfile(path):
        os.remove(path)


def root_run(cmd, cwd=None):
    run_cwd = cwd if cwd else base_dir()
    if root_platform() == "win32":
        process = subprocess.run(
            cmd,
            cwd=run_cwd,
            shell=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        return process.returncode

    old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        process = subprocess.run(
            cmd,
            cwd=run_cwd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            preexec_fn=root_child_default_sigint,
        )
    finally:
        signal.signal(signal.SIGINT, old_handler)
    return process.returncode


def root_run_xmake(args, cwd=None):
    return root_run([toolchain_xmake()] + args, cwd if cwd else root_dir())


def root_run_xmake_build(out_dir, mode, cwd=None):
    xmake_cwd = cwd if cwd else root_dir()
    code = root_run_xmake(
        ["f", "-o", out_dir, "-m", mode],
        xmake_cwd
    )
    if code != 0:
        return code
    return root_run_xmake(["build"], xmake_cwd)


def root_run_openocd(args, cwd=None):
    return root_run([toolchain_openocd()] + args, cwd)


def openocd_interface_cfg():
    return "interface/stlink.cfg"


def openocd_target_cfg():
    return "target/stm32f4x.cfg"


def openocd_base_args():
    return [
        "-f", openocd_interface_cfg(),
        "-f", openocd_target_cfg(),
    ]


def toolchain_gdb():
    if root_platform() == "win32":
        return root_env("ROOT_GDB", "arm-none-eabi-gdb.exe")
    return root_env("ROOT_GDB", "gdb-multiarch")


def openocd_pid_file():
    return os.path.join(target_dir(), "openocd.pid")


def root_run_background(cmd, cwd=None):
    run_cwd = cwd if cwd else base_dir()
    if root_platform() == "win32":
        flags = (
            subprocess.CREATE_NEW_PROCESS_GROUP |
            subprocess.DETACHED_PROCESS
        )
        process = subprocess.Popen(
            cmd,
            cwd=run_cwd,
            creationflags=flags,
        )
    else:
        process = subprocess.Popen(
            cmd,
            cwd=run_cwd,
            start_new_session=True,
        )
    return process.pid


def root_process_alive(pid):
    if root_platform() == "win32":
        result = subprocess.run(
            ["tasklist", "/FI", "PID eq " + str(pid)],
            capture_output=True,
            text=True,
        )
        return str(pid) in result.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def root_write_pid(path, pid):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        handle.write(str(pid))


def root_read_pid(path):
    if not os.path.isfile(path):
        return None
    with open(path) as handle:
        content = handle.read().strip()
    if not content:
        return None
    try:
        return int(content)
    except ValueError:
        return None


def root_append_pid(path, pid):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as handle:
        handle.write(str(pid) + "\n")


def root_read_pids(path):
    if not os.path.isfile(path):
        return []
    with open(path) as handle:
        lines = handle.read().splitlines()
    pids = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            pids.append(int(line))
        except ValueError:
            pass
    return pids


def app_elf_path(mode):
    if mode == "debug":
        return os.path.join(debug_dir(), "app.elf")
    return os.path.join(release_dir(), "app.elf")


def root_confirm(prompt):
    answer = input(prompt + " [y/N] ").strip().lower()
    return answer == "y"


def root_run_rmdir(path):
    if not root_confirm("remove " + root_relpath(path) + " ?"):
        return 1
    if root_platform() == "win32":
        return root_run(["rmdir", "/s", "/q", path])
    return root_run(["rm", "-rf", path])


def root_fail(code):
    if code != 0:
        sys.exit(code)