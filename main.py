from anytree import Node, RenderTree, findall_by_attr, PreOrderIter

# global to identify the type
typeOfAllocation = 0

# disk size
DISK_SIZE = 500

# holds disk blocks (0s and 1s)
DISK_BLOCKS = "11111010101010111111" + "0" * 475 + "11110"

# holds all ranges of allocated and unallocated blocks
disk_space = {
    "0": [],
    "1": [],
}

# a tree holds all directories/files objects
root = Node("root", fileType="d")


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


# get the full path from a leaf node
def get_file_path(leaf_node, file_path=""):
    if leaf_node.is_root:
        return "root/" + '/'.join(file_path.split()[::-1])
    else:
        file_path += leaf_node.name + " "
        return get_file_path(leaf_node.parent, file_path)


def create_file(path, blocks_num):
    file_name = path.split('/')[-1]
    parent_name = path.split('/')[-2]
    parent_path = '/'.join(path.split('/')[:-1])

    file_parent_found = False

    # get all matching nodes
    matches = findall_by_attr(root, parent_name)
    # if there is a match
    if matches:
        # see if the matching path is the required path
        for match in matches:
            if parent_path == get_file_path(match) or parent_name == "root":
                # check if folder name already exists in the same path
                siblings = [child.name for child in match.children if child.fileType == "f"]

                if file_name in siblings:
                    print("Error: File with the same name already exists")
                else:
                    if match.fileType == "d":
                        Node(file_name, parent=match, fileType="f")
                        print("FILE CREATED SUCCESSFULLY")
                        return
                    else:
                        file_parent_found = True
            else:
                print("ERROR: %s/ path doesn't exist!" % parent_path)
                print(get_file_path(match))
    else:
        print("ERROR: %s/ path doesn't exist!" % parent_path)

    if file_parent_found:
        print("ERROR: %s is a file not a directory" % parent_name)


def create_folder(path):
    folder_name = path.split('/')[-1]
    parent_name = path.split('/')[-2]
    parent_path = '/'.join(path.split('/')[:-1])

    # get all matching nodes
    matches = findall_by_attr(root, parent_name)
    # if there is a match
    if matches:
        # see if the matching path is the required path
        for match in matches:
            if parent_path == get_file_path(match) or parent_name == "root":
                # check if folder name already exists in the same path
                siblings = [child.name for child in match.children if child.fileType == "d"]

                if folder_name in siblings:
                    print("Error: File with the same name already exists")
                else:
                    if match.fileType == "d":
                        Node(folder_name, parent=match, fileType="d")
                        print("FOLDER CREATED SUCCESSFULLY")
                    else:
                        print("ERROR: %s is a file not a directory" % parent_name)
            else:
                print("ERROR: %s/ path doesn't exist!" % parent_path)
                print(get_file_path(match))
    else:
        print("ERROR: %s/ path doesn't exist!" % parent_path)


def delete_file(path):
    if path != "root":
        filename = path.split('/')[-1]
    else:
        print("Error: You cannot delete root directory")
        return

    dir_only_found = False

    # get all matching nodes
    matches = findall_by_attr(root, filename)
    # if there is a match
    if matches:
        # see if the matching path is the required path
        for match in matches:
            if path == get_file_path(match):
                if match.fileType == "f":
                    match.parent = None
                    print("FILE DELETED SUCCESSFULLY")
                    return
                else:
                    dir_only_found = True
            else:
                print("ERROR: File not found!")
    else:
        print("ERROR: File not found!")

    if dir_only_found:
        print("ERROR: this is a directory you should use \"DeleteFolder\" command")


def delete_folder(path):
    if path != "root":
        dirname = path.split('/')[-1]
    else:
        print("Error: You cannot delete root directory")
        return

    file_only_found = False

    # get all matching nodes
    matches = findall_by_attr(root, dirname)
    # if there is a match
    if matches:
        # see if the matching path is the required path
        for match in matches:
            if path == get_file_path(match):
                if match.fileType == "d":
                    match.parent = None
                    print("DIRECTORY DELETED SUCCESSFULLY")
                    return
                else:
                    file_only_found = True
            else:
                print("ERROR: Folder not found!")
    else:
        print("ERROR: Folder not found!")

    if file_only_found:
        print("ERROR: this is a file you should use \"DeleteFile\" command")


def get_block_ranges():
    global disk_space

    # resetting
    disk_space["0"] = []
    disk_space["1"] = []

    start = 0
    end = 0

    while end != DISK_SIZE:
        curr_block = DISK_BLOCKS[start]
        if curr_block == "0":
            wall = "1"
        else:
            wall = "0"

        # gets the end of blocks chunk
        end = DISK_BLOCKS.find(wall, start)
        # if no wall blocking the way then it's the end of disk
        if end == -1:
            end = DISK_SIZE
        # storing the ranges or block numbers in the corresponding type
        if start != end - 1:
            disk_space[curr_block].append([start, end - 1])
        else:
            disk_space[curr_block].append(start)

        start = end  # moving pointer forward


def display_disk_status():
    bit = 1
    for block in DISK_BLOCKS:
        print(block, end='')
        if bit % 100 == 0:
            print('')
        bit += 1

    print("Empty space: %d KB" % DISK_BLOCKS.count('0'))
    print("Allocated space: %d KB" % DISK_BLOCKS.count('1'))
    print("Empty blocks in disk: %s" % disk_space["0"])
    print("Allocated blocks in disk: %s" % disk_space["1"])


def display_disk_structure():
    for pre, _, node in RenderTree(root):
        print("%s[%s] %s" % (pre, node.fileType, node.name))


def load_vfs_file():
    global root
    tmp_parent = root

    with open("DiskStructure.vfs", "r", encoding='utf-8') as f:
        while True:
            line = f.readline().strip()

            if line == "---":
                break

            # getting the file type letter d or f and trimming
            file_type = line[0]
            line = line[2:]

            path = line.split("/")
            # iterate on each filename in the path
            for filename in path:
                # if node not found then create it as tmp_child
                if not findall_by_attr(root, filename):
                    tmp_child = Node(filename, parent=tmp_parent, fileType="d")
                # save current node as tmp_parent to be used as a parent to the next node (if exists)
                tmp_parent = findall_by_attr(root, filename)[0]

            # if it's a file change the file attribute to file
            if file_type == "f":
                tmp_child.fileType = "f"


def save_vfs_file():

    with open("DiskStructure.vfs", "w", encoding='utf-8') as f:
        # iterate on all nodes
        for node in PreOrderIter(root):
            # if it's a leaf node get type and full path and save them
            if node.is_leaf:
                path = get_file_path(node)
                f.write(node.fileType + " ")
                f.write(path)
                f.write('\n')

        # separator for end of the tree section
        f.write('---\n')


def main():

    # Determine the type of allocation at first
    # to know the VFS file's structure
    allocation_type()

    # loading data from VFS file
    load_vfs_file()

    while True:
        cmd = input("$ ")
        cmd = cmd.split()

        get_block_ranges()  # getting the ranges of allocated/unallocated bocks

        # ex: CreateFile root/file.txt 100
        if cmd[0] == "CreateFile":
            if len(cmd) == 3:
                create_file(cmd[1], int(cmd[2]))
            else:
                print("Usage: CreateFile <path> <number-of-blocks>")

        # ex: CreateFolder root/folder1
        elif cmd[0] == "CreateFolder":
            if len(cmd) == 2:
                create_folder(cmd[1])
            else:
                print("Usage: CreateFolder <path>")

        # ex: DeleteFile root/folder1/file.txt
        elif cmd[0] == "DeleteFile":
            if len(cmd) == 2:
                delete_file(cmd[1])
            else:
                print("Usage: DeleteFile <path>")

        # ex: DeleteFolder root/folder1
        elif cmd[0] == "DeleteFolder":
            if len(cmd) == 2:
                delete_folder(cmd[1])
            else:
                print("Usage: DeleteFolder <path>")

        # ex: DisplayDiskStatus
        elif cmd[0] == "DisplayDiskStatus":
            display_disk_status()

        # ex: DisplayDiskStructure
        elif cmd[0] == "DisplayDiskStructure":
            display_disk_structure()

        elif cmd[0] == "exit":
            break

        else:
            print("ERROR: Unknown command!")

    # saving data to VFS file
    save_vfs_file()


if __name__ == '__main__':
    main()
