class File:
    deleted = False

    def __init__(self, path, blocks):
        self.file_path = path
        self.allocated_blocks = blocks


class Directory:
    files = []
    sub_directories = []
    deleted = False

    def __init__(self, path):
        self.directory_path = path


def create_file(path, blocks_num):
    return


def create_folder(path):
    return


def delete_file(path):
    return


def delete_folder(path):
    return


def display_disk_status():
    return


def display_disk_structure():
    return


def main():
    cmd = ""

    while cmd != "exit":
        cmd = input("$ ")
        cmd.split()

        # ex: CreateFile root/file.txt 100
        if cmd[0] == "CreateFile":
            create_file(cmd[1], int(cmd[2]))

        # ex: CreateFolder root/folder1
        elif cmd[0] == "CreateFolder":
            create_folder(cmd[1])

        # ex: DeleteFile root/folder1/file.txt
        elif cmd[0] == "DeleteFile":
            delete_file(cmd[1])

        # ex: DeleteFolder root/folder1
        elif cmd[0] == "DeleteFolder":
            delete_folder(cmd[1])

        # ex: DisplayDiskStatus
        elif cmd[0] == "DisplayDiskStatus":
            display_disk_status()

        # ex: DisplayDiskStructure
        elif cmd[0] == "DisplayDiskStructure":
            display_disk_structure()


if __name__ == '__main__':
    main()