import shlex


def base_menu_print(path, entries):
    print(path)
    for command, label in entries:
        print(command + " -- " + label)


def base_help_print(title, entries):
    print(title)
    for command, description in entries:
        print(command + " -- " + description)


def base_command_split(line):
    try:
        return shlex.split(line)
    except ValueError:
        return []


def base_command_key(line):
    parts = base_command_split(line)
    if not parts:
        return ""
    return parts[0]


def base_loop(prompt, menu, handlers, exit_command="x"):
    menu()
    while True:
        line = input(prompt).strip()
        parts = base_command_split(line)
        if not parts:
            continue
        command = parts[0]
        if command == exit_command:
            return 0
        handler = handlers.get(command)
        if handler is None:
            continue
        code = handler(parts[1:])
        if code is not None and code != 0:
            return code