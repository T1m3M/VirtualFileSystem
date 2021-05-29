from anytree import Node, RenderTree, findall_by_attr, PreOrderIter

# global to identify the type
typeOfAllocation = 0


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
    # Check if path already exists
    # No file with same name already created there
    return


def create_folder(path):
    return


def delete_file(path):
    if path != "root":
        filename = path.split('/')[-1]
    else:
        print("Error: You cannot delete root directory")
        return

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
                else:
                    print("ERROR: this is a directory you should use \"DeleteFolder\" command")

    else:
        print("ERROR: File not found!")


def delete_folder(path):
    delete_file(path)


def display_disk_status():
    return


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
            break

        else:
            print("ERROR: Unknown command!")

    # saving data to VFS file
    save_vfs_file()


if __name__ == '__main__':
    main()
