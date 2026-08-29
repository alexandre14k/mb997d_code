import subprocess
import threading
import time

import filter
import root


server_process = None
server_thread = None
server_running = False


def server_openocd_command():
    return [
        root.toolchain_openocd(),
        "-f", root.openocd_interface_cfg(),
        "-f", root.openocd_target_cfg(),
    ]


def server_output_loop():
    while server_running:
        process = server_process

        if process is None:
            return

        line = process.stdout.readline()

        if not line:
            if process.poll() is not None:
                return
            continue

        message = filter.filter_openocd_message(line)

        if message is not None:
            print(message)


def server_start():
    global server_process
    global server_thread
    global server_running

    server_stop()

    server_process = subprocess.Popen(
        server_openocd_command(),
        cwd=root.root_dir(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    server_running = True

    server_thread = threading.Thread(
        target=server_output_loop,
        daemon=True,
    )

    server_thread.start()

    time.sleep(0.3)

    if server_process.poll() is not None:
        server_stop()
        return 1

    root.root_write_pid(
        root.openocd_pid_file(),
        server_process.pid,
    )

    return 0


def server_stop():
    global server_process
    global server_thread
    global server_running

    server_running = False

    process = server_process

    if process is not None:
        if process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            except OSError:
                pass

    pid = root.root_read_pid(root.openocd_pid_file())

    if pid and root.root_process_alive(pid):
        root.root_kill_process(pid)

    root.root_remove_pid(root.openocd_pid_file())

    if server_thread is not None:
        server_thread.join(timeout=1.0)

    server_process = None
    server_thread = None

    return 0


def server_reset():
    server_stop()
    return server_start()