import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("255.255.255.255", 3269))

LIST_FILE = "/dev/shm/.embedMAS/neighbors/list"

while True:
    data, addr = sock.recvfrom(256)

    entry = data.decode().strip()

    if not entry:
        continue

    name = entry.split(maxsplit=1)[0]

    with open(LIST_FILE, "r") as file:
        lines = file.readlines()

    found = False
    changed = False
    new_lines = []

    for line in lines:
        current = line.strip()

        if not current:
            continue

        current_name = current.split(maxsplit=1)[0]

        if current_name == name:
            found = True

            if current == entry:
                # Já existe exatamente igual.
                new_lines.append(line)
            else:
                # Existe, mas mudou.
                # Não adiciona a linha antiga.
                changed = True
        else:
            new_lines.append(line)

    if not found:
        with open(LIST_FILE, "a") as file:
            file.write(entry + "\n")

    elif changed:
        new_lines.append(entry + "\n")

        with open(LIST_FILE, "w") as file:
            file.writelines(new_lines)