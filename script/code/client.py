import queue
import subprocess
import threading

import filter
import root


client_command_queue = queue.Queue()
client_response_event = threading.Event()

client_process = None
client_thread = None
client_output_thread = None

client_running = False
client_connected_state = False
client_responsive_state = False


def client_connected():
    return client_connected_state


def client_responsive():
    return (
        client_running
        and client_process is not None
        and client_process.poll() is None
        and client_responsive_state
    )


def client_filter_message(line):
    return filter.filter_gdb_message(line)


def client_gdb_command():
    return [
        root.toolchain_gdb(),
        "-q",
        root.app_elf_path("debug"),
        "-ex", "set pagination off",
        "-ex", "set confirm off",
    ]


def client_output_print(buffer):
    if not buffer:
        return

    lines = buffer.splitlines()

    for line in lines:
        message = client_filter_message(line)

        if message is not None:
            if message.strip() == "...":
                print("...")
            else:
                print(message)


def client_output_loop():
    global client_responsive_state

    buffer = ""
    prompt = "(gdb) "

    while client_running:
        process = client_process

        if process is None:
            return

        char = process.stdout.read(1)

        if not char:
            if process.poll() is not None:
                return
            continue

        buffer += char

        if buffer.endswith(prompt):
            content = buffer[:-len(prompt)]
            client_output_print(content)

            buffer = ""

            client_responsive_state = True
            client_response_event.set()
            continue

        if buffer.endswith("(gdb)"):
            content = buffer[:-5]
            client_output_print(content)

            buffer = ""

            client_responsive_state = True
            client_response_event.set()
            continue

        if "\n" in buffer:
            lines = buffer.split("\n")
            buffer = lines.pop()

            for line in lines:
                message = client_filter_message(line)

                if message is not None:
                    print(message)


def client_command_loop():
    while client_running:
        try:
            command = client_command_queue.get(
                timeout=0.1,
            )
        except queue.Empty:
            continue

        if command is None:
            return

        process = client_process

        if process is None:
            continue

        try:
            process.stdin.write(command + "\n")
            process.stdin.flush()
        except (BrokenPipeError, OSError):
            return


def client_start():
    global client_process
    global client_thread
    global client_output_thread
    global client_running
    global client_connected_state
    global client_responsive_state

    if client_running:
        return 0

    client_connected_state = False
    client_responsive_state = False

    client_response_event.clear()

    while True:
        try:
            client_command_queue.get_nowait()
        except queue.Empty:
            break

    client_process = subprocess.Popen(
        client_gdb_command(),
        cwd=root.root_dir(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    client_running = True

    client_output_thread = threading.Thread(
        target=client_output_loop,
        daemon=True,
    )

    client_thread = threading.Thread(
        target=client_command_loop,
        daemon=True,
    )

    client_output_thread.start()
    client_thread.start()

    client_response_event.clear()

    return 0


def client_send(command):
    global client_responsive_state
    global client_connected_state

    if not client_running:
        return 1

    client_responsive_state = False
    client_response_event.clear()

    client_command_queue.put(command)

    if not client_response_event.wait(timeout=10.0):
        return 1

    if command == "target extended-remote localhost:3333":
        client_connected_state = True

    if command == "disconnect":
        client_connected_state = False

    return 0


def client_stop():
    global client_process
    global client_thread
    global client_output_thread
    global client_running
    global client_connected_state
    global client_responsive_state

    process = client_process

    client_running = False
    client_connected_state = False
    client_responsive_state = False

    client_response_event.clear()

    while True:
        try:
            client_command_queue.get_nowait()
        except queue.Empty:
            break

    if process is not None:
        try:
            process.stdin.close()
        except (BrokenPipeError, OSError):
            pass

        try:
            process.terminate()
        except OSError:
            pass

        try:
            process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except OSError:
                pass

            try:
                process.wait()
            except OSError:
                pass

    if client_thread is not None:
        client_thread.join(timeout=1.0)

    if client_output_thread is not None:
        client_output_thread.join(timeout=1.0)

    client_process = None
    client_thread = None
    client_output_thread = None

    return 0