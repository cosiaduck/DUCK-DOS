import os
import shutil

CD = "C:\\"

def error():
    print("Bad command or file name")

def read_file(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            print(f.read())
    else:
        print("File not found")

def handle_read(args, current_directory):
    if len(args) >= 1:
        for arg in args:
            read_file(resolve_path(current_directory, arg))
        return current_directory
    error()
    return current_directory


def write_file(filename, content):
    with open(filename, "w") as f:
        f.writelines(content)

def handle_write(args, current_directory):
    if len(args) == 2:
        write_file(resolve_path(current_directory, args[0]), args[1])
        return current_directory
    error()
    return current_directory


def read_directory(directory):
    dir_count = 0
    file_count = 0
    if os.path.exists(directory):
        for path in os.listdir(directory):
            try:
                full_path = os.path.join(directory, path)
                if os.path.isdir(full_path):
                    print("<DIR>    " + path)
                    dir_count += 1
                if os.path.isfile(full_path):
                    print("    <FILE>    " + path +"    size:   " + str(os.path.getsize(full_path)))
                    file_count += 1
            except PermissionError:
                continue
    else:
        print("Directory not found")
    return dir_count, file_count

def handle_dir(args,current_directory):
    if len(args) == 1:
        dir_count, file_count = read_directory(resolve_path(current_directory, args[0]))
        print("DIR listed: " + str(dir_count))
        print("FILE listed: " + str(file_count))
        return current_directory
    elif len(args) == 0:
        dir_count, file_count = read_directory_recursively(resolve_path(current_directory, current_directory), 0, 0)
        print("DIR listed: " + str(dir_count))
        print("FILE listed: " + str(file_count))
        return current_directory
    error()
    return current_directory

def handle_dir_recursive(args, current_directory):
    if len(args) == 1:
        dir_count, file_count = read_directory_recursively(resolve_path(current_directory, args[0]), 0, 0)
        print("DIR listed: " + str(dir_count))
        print("FILE listed: " + str(file_count))
        return current_directory
    elif len(args) == 0:
        dir_count, file_count = read_directory_recursively(resolve_path(current_directory, current_directory), 0, 0)
        print("DIR listed: " + str(dir_count))
        print("FILE listed: " + str(file_count))
        return current_directory
    error()
    return current_directory

def read_directory_recursively(directory, dir_count, file_count):
    if os.path.exists(directory):
        for path in os.listdir(directory):
            try:
                full_path = os.path.join(directory, path)
                if os.path.isdir(full_path):
                    print("<DIR>    " + path)
                    dir_count += 1
                    child_dir, child_file = read_directory_recursively(full_path, 0, 0)
                    dir_count += child_dir
                    file_count += child_file
            except PermissionError:
                continue
            try:
                if os.path.isfile(full_path):
                    print("    <FILE>    " + path + "    size:   " + str(os.path.getsize(full_path)))
                    file_count += 1
            except PermissionError:
                continue

    else:
        print("Directory not found")
    return dir_count, file_count


def help():
    print("DUCK-DOS COMMANDS \n \n"
          "READ <file> [file]; [file];...      Read (a) file(s) \n"
          "WRITE <file>                        Write to a file \n"
          "DIR [directory]                     List files \n"
          "EXIT                                Exit DUCK-DOS \n"
          "HELP                                Show this message \n"
          "COPY <source> <destination>         Copy source to destination \n"
          "DEL <file> [file] [file] ...        Delete file(s) \n"
          "DELDIR <directory> [directory]      Delete directories \n"
          "REN <old_file> <new_file>           Rename old file \n"
          "RENDIR <old_dir> <new_dir>          Rename old directory \n"
          "MKDIR <dir>                         Make a new DIR\n"
          "RUN <file.duck>                     Run DUCK-DOS code\n")

def handle_help(args, current_directory):
    help()
    return current_directory

def resolve_path(cd, path):
    if os.path.isabs(path):
        return path

    return os.path.join(cd, path)

def handle_cd(args, current_directory):
    if len(args) == 1:
        return resolve_path(current_directory, args[0])

    error()
    return current_directory

def copy(source, destination):
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(source))
    if os.path.exists(source):
        with open(source) as f:
            content = f.read()
        with open(destination, "w") as f:
            f.write(content)

def handle_copy(args, current_directory):
    if len(args) == 2:
        copy(resolve_path(current_directory, args[0]), resolve_path(current_directory, args[1]))
        return current_directory
    error()
    return current_directory

def delete(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            print("cannot delete directory")
            print("please use DELDIR instead")
        else:
            print("Deleting file: " + path)
            os.remove(path)
            print("Deleted: " + path)

def delete_dir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            print("Deleting directory: " + path)
            shutil.rmtree(path)
            print("Deleted: " + path)

def handle_delete(args, current_directory):
    if len(args) == 1:
        delete(resolve_path(current_directory, args[0]))
        return current_directory
    error()
    return current_directory

def handle_delete_dir(args, current_directory):
    if len(args) == 1:
        delete_dir(resolve_path(current_directory, args[0]))
        return current_directory
    error()
    return current_directory

def rename(old_file, new_file):
    if os.path.exists(old_file):
        if os.path.isdir(old_file):
            print("cannot rename directory to file")
            print("please use RENDIR instead")
        else:
            print("renamed file: " + old_file + "to: " + new_file)
            os.rename(old_file, new_file)
    else:
        print("File not found: " + old_file)

def rename_dir(old_dir, new_dir):
    if os.path.exists(old_dir):
        if os.path.isdir(old_dir):
            print("renamed directory: " + old_dir + "to: " + new_dir)
            os.rename(old_dir, new_dir)
        else:
            print("cannot rename file to directory")
            print("please use REN instead")

def handle_ren_dir(args, current_directory):
    if len(args) == 2:
        rename_dir(args[0], args[1])
        return current_directory
    error()
    return current_directory

def handle_ren(args, current_directory):
    if len(args) == 2:
        rename(args[0], args[1])
        return current_directory
    error()
    return current_directory

def make_dir(cd,path):
    if not os.path.exists(os.path.join(cd, path)):
        os.mkdir(os.path.join(cd, path))
    else:
        print("Directory already exists: " + path)

def handle_make_dir(args, current_directory):
    if len(args) == 1:
        make_dir(current_directory, args[0])
        return current_directory
    error()
    return current_directory

def handle_cls(args, current_directory):
    os.system("cls")
    return current_directory

def handle_exit(args, current_directory):
    print("Thank you for using DUCK-DOS")
    exit()


def execute_command(command, current_directory):
    command[0] = command[0].upper()
    handler = commands.get(command[0])

    if handler:
        return handler(command[1:], current_directory)

    error()
    return current_directory

def run(path, current_directory):
    path = resolve_path(current_directory, path)

    with open(path, "r") as f:
        lines = f.readlines()

        for line in lines:
            line = line.rstrip("\n")
            line = line.split()
            if len(line) != 0:
                current_directory = execute_command(line, current_directory)

    return current_directory

def handle_run(args, current_directory):
    if len(args) == 1:
        run(args[0], current_directory)
    return current_directory

commands = {
    "CLS": handle_cls,
    "HELP": handle_help,
    "CD": handle_cd,
    "MKDIR": handle_make_dir,
    "READ": handle_read,
    "REN": handle_ren,
    "RENDIR": handle_ren_dir,
    "WRITE": handle_write,
    "DEL": handle_delete,
    "DELDIR": handle_delete_dir,
    "COPY": handle_copy,
    "DIR": handle_dir,
    "DIRS": handle_dir_recursive,
    "EXIT": handle_exit,
    "RUN": handle_run,
}

while True:
    command = input(CD + ">").split()
    if len(command) != 0:
        CD = execute_command(command, CD)
