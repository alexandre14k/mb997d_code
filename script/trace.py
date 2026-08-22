import sys
import root


def trace_openocd_cmd():
    return [
        root.toolchain_openocd(),
        "-f", root.openocd_interface_cfg(),
        "-f", root.openocd_target_cfg(),
    ]


def trace_gdb_cmd():
    return [root.toolchain_gdb(), root.app_elf_path("debug")]


def trace_running_pids():
    pids = root.root_read_pids(root.openocd_pid_file())
    return [pid for pid in pids if root.root_process_alive(pid)]


def trace_is_running():
    return len(trace_running_pids()) > 0


def trace_start():
    pid = root.root_run_background(
        trace_openocd_cmd(), root.root_dir()
    )
    root.root_append_pid(root.openocd_pid_file(), pid)
    print("debugger started, pid " + str(pid))
    return 0


def trace_stop():
    pids = root.root_read_pids(root.openocd_pid_file())
    if not pids:
        print("debugger not running")
        return 0
    killed = 0
    for pid in pids:
        if root.root_process_alive(pid):
            root.root_kill_process(pid)
            killed += 1
    root.root_remove_pid(root.openocd_pid_file())
    print("debugger stopped, killed " + str(killed) + " instance(s)")
    return 0


def trace_trace():
    if not trace_is_running():
        print("debugger not running, use d first")
        return 1
    return root.root_run(trace_gdb_cmd(), root.root_dir())


def trace_main():
    if len(sys.argv) < 2:
        print("usage: trace.py [d|t|q]")
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "d":
        code = trace_start()
    elif mode == "t":
        code = trace_trace()
    elif mode == "q":
        code = trace_stop()
    else:
        print("usage: trace.py [d|t|q]")
        code = 1
    root.root_fail(code)


if __name__ == "__main__":
    trace_main()