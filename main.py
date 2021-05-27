# global to identify the type
typeOfAllocation = 0


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


def allocation_type():
    global typeOfAllocation

    alloc_type = 0

    while alloc_type == 0:
        print("\nChoose an allocation technique:")
        print("[1] Contiguous Allocation")
        print("[2] Indexed Allocation")
        print("[3] Linked Allocation")

        try:
            alloc_type = int(input("> "))
        except ValueError:
            alloc_type = 0
            print("ERROR: Incorrect type!")
            continue

        if alloc_type != 1 and alloc_type != 2 and alloc_type != 3:
            alloc_type = 0
            print("ERROR: You can only choose 1, 2 or 3")
            continue

        typeOfAllocation = alloc_type


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

    # Determine the type of allocation at first
    # to know the VFS file's structure
    allocation_type()

    while True:
        cmd = input("$ ")
        cmd = cmd.split()

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

        elif cmd[0] == "exit":
            return

        else:
            print("ERROR: Unknown command!")


if __name__ == '__main__':
    main()
