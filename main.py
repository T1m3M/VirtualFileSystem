from anytree import Node, RenderTree, findall_by_attr, PreOrderIter
from random import randint

# global to identify the type
typeOfAllocation = 0

# disk size
DISK_SIZE = 500

# holds disk blocks (0s and 1s)
DISK_BLOCKS = "0" * DISK_SIZE

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


def contiguous_alloc(blocks_num):
    global DISK_BLOCKS
    all_blocks = [block for block in DISK_BLOCKS]

    for space in disk_space["0"]:
        free_space = space[1] - space[0] + 1
        # if there exists enough contiguous space
        if free_space >= blocks_num:
            for i in range(0, blocks_num):
                all_blocks[space[0] + i] = "1"  # allocating

            DISK_BLOCKS = ''.join(all_blocks)
            return [space[0], blocks_num]  # for saving/loading

    return False


def find_empty_block():
    rand_block = randint(0, DISK_SIZE - 1)
    while DISK_BLOCKS[rand_block] == "1":
        rand_block = randint(0, DISK_SIZE - 1)
    return rand_block


def indexed_alloc(blocks_num):
    global DISK_BLOCKS
    all_blocks = [block for block in DISK_BLOCKS]
    space_available = DISK_BLOCKS.count("0")
    indexes_table = []

    # if there exists enough space for blocks + index table block
    if space_available >= blocks_num + 1:
        for i in range(0, blocks_num):
            # getting an empty random block in free space
            empty_block_index = find_empty_block()
            all_blocks[empty_block_index] = "1"  # allocating
            DISK_BLOCKS = ''.join(all_blocks)  # updating the actual disk
            indexes_table.append(empty_block_index)

        table_block_index = find_empty_block()  # allocating block to store table
        all_blocks[table_block_index] = "1"

        DISK_BLOCKS = ''.join(all_blocks)
        return [table_block_index, indexes_table]  # for saving/loading

    return False


def linked_alloc(blocks_num):
    global DISK_BLOCKS
    all_blocks = [block for block in DISK_BLOCKS]
    space_available = DISK_BLOCKS.count("0")
    linked_list = []
    prev_block_index = 0

    # if there exists enough space for blocks
    if space_available >= blocks_num:
        for i in range(0, blocks_num):
            # getting an empty random block in free space
            empty_block_index = find_empty_block()
            all_blocks[empty_block_index] = "1"  # allocating
            DISK_BLOCKS = ''.join(all_blocks)  # updating the actual disk

            if i != 0:
                linked_list.append([prev_block_index, empty_block_index])

            prev_block_index = empty_block_index

        linked_list.append([prev_block_index, None])
        DISK_BLOCKS = ''.join(all_blocks)
        return linked_list  # for saving/loading

    return False


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

                        # ----------[ Contiguous Allocation ]----------
                        if typeOfAllocation == 1:
                            allocated = contiguous_alloc(blocks_num)
                        # -----------[ Indexed Allocation ]------------
                        elif typeOfAllocation == 2:
                            allocated = indexed_alloc(blocks_num)
                        # ------------[ Linked Allocation ]------------
                        else:
                            allocated = linked_alloc(blocks_num)

                        if allocated:
                            Node(file_name, parent=match, fileType="f", allocBlocks=allocated)
                            print("FILE CREATED SUCCESSFULLY")
                        else:
                            print("ERROR: no such space exists to create the file")

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


def contiguous_dealloc(file_node):
    global DISK_BLOCKS

    start = file_node.allocBlocks[0]
    length = file_node.allocBlocks[1]
    all_blocks = [block for block in DISK_BLOCKS]
    # deallocating the space in disk
    for i in range(0, length):
        all_blocks[start + i] = "0"

    DISK_BLOCKS = ''.join(all_blocks)


def indexed_dealloc(file_node):
    global DISK_BLOCKS

    table_block = file_node.allocBlocks[0]
    indexes = file_node.allocBlocks[1]
    all_blocks = [block for block in DISK_BLOCKS]

    # deallocating the indexes in disk
    for index in indexes:
        all_blocks[index] = "0"

    # deallocating the block which holds the table
    all_blocks[table_block] = "0"
    DISK_BLOCKS = ''.join(all_blocks)


def linked_dealloc(file_node):
    global DISK_BLOCKS

    linked_list = file_node.allocBlocks
    all_blocks = [block for block in DISK_BLOCKS]

    # getting the heads only from the linked list
    blocks = [single_list[0] for single_list in linked_list]

    # deallocating the indexes in disk
    for block in blocks:
        all_blocks[block] = "0"

    DISK_BLOCKS = ''.join(all_blocks)


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

                    # ----------[ Contiguous De-allocation ]----------
                    if typeOfAllocation == 1:
                        contiguous_dealloc(match)
                    # -----------[ Indexed De-allocation ]------------
                    elif typeOfAllocation == 2:
                        indexed_dealloc(match)
                    # ------------[ Linked De-allocation ]------------
                    else:
                        linked_dealloc(match)

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


def get_child_files(path, node, files=[]):
    for child in node.children:
        child_path = path + '/' + child.name
        if child.fileType == "f":
            files.append(child_path)
        else:
            get_child_files(child_path, child)

    return files


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
                    # deallocate children files
                    child_files = get_child_files(path, match)
                    for child_file in child_files:
                        delete_file(child_file)

                    # detach from tree
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
        # storing the ranges in the corresponding type
        disk_space[curr_block].append([start, end - 1])

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


def find_node(path):
    node_name = path.split('/')[-1]

    # get all matching nodes
    matches = findall_by_attr(root, node_name)

    # if there is a match
    if matches:
        # see if the matching path is the required path
        for match in matches:
            if path == get_file_path(match):
                return match
    return 0


def get_start_offset():
    template = 0  # flag to indicate which portion for loading
    offset = 0

    with open("DiskStructure.vfs", "r", encoding='utf-8') as f:
        line = f.readline()
        offset += len(line) + 1

        # Seeking to the starting point
        if typeOfAllocation != 1:
            while True:
                if line == "###\n":
                    if typeOfAllocation == 2:
                        break
                    elif typeOfAllocation == 3 and template == 1:
                        break
                    template = 1  # remark the first ### found

                line = f.readline()
                offset += len(line) + 1
        else:
            offset = 0

    return offset


def load_vfs_file():
    global root, DISK_BLOCKS
    tmp_parent = root

    with open("DiskStructure.vfs", "r", encoding='utf-8') as f:
        # get the start position in file based on allocation type
        offset = get_start_offset()
        f.seek(offset)

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

        # loading the blocks section
        DISK_BLOCKS = f.readline().strip()

        f.readline().strip()  # to skip the section's separator "---"
        while True:
            line = f.readline().strip()
            if line == "###":
                break

            file_info = line.split()
            match_node = find_node(file_info[0])

            # ----------[ Contiguous allocation ]----------
            if typeOfAllocation == 1:
                alloc_ = [int(x) for x in file_info[1:]]
            # -----------[ Indexed allocation ]------------
            elif typeOfAllocation == 2:
                table_block = int(file_info[1])
                line = f.readline().strip()
                indexes = [int(x) for x in line.split()]
                alloc_ = [table_block, indexes]
            # ------------[ Linked allocation ]------------
            else:
                line = f.readline().strip()
                linked_list = []
                links = line.split()
                # restoring the linked list from the line
                for link in links:
                    try:
                        link_list = [int(x) for x in link.split("-")]
                    except ValueError:
                        link_list = [int(link.split("-")[0]), None]
                    linked_list.append(link_list)

                alloc_ = linked_list

            match_node.allocBlocks = alloc_


def get_lines_and_index():
    # reading the hole vfs file into a list
    with open("DiskStructure.vfs", "r", encoding='utf-8') as f:
        contents = f.readlines()

    # getting indexes of ### separator
    get_separators_indexes = [i for (y, i) in zip(contents, range(len(contents))) if "###\n" == y]

    if typeOfAllocation == 1:
        for i in range(get_separators_indexes[0] + 1):
            contents.pop(0)

        return 0, contents
    elif typeOfAllocation == 2:
        for i in range(get_separators_indexes[1] - get_separators_indexes[0]):
            contents.pop(get_separators_indexes[0] + 1)

        return get_separators_indexes[0] + 1, contents
    else:
        for i in range(get_separators_indexes[2] - get_separators_indexes[1]):
            contents.pop(get_separators_indexes[1] + 1)

        return get_separators_indexes[1] + 1, contents


def save_vfs_file():

    # getting the array trimmed from the needed section
    # to record the new updated without affecting other algorithms
    # and starting index in that array
    start_offset, file_contents = get_lines_and_index()
    offset = start_offset

    # iterate on all nodes
    for node in PreOrderIter(root):
        # if it's a leaf node get type and full path and save them
        if node.is_leaf:
            path = get_file_path(node)
            file_contents.insert(offset, node.fileType + " " + path + '\n')
            offset += 1

    # separator for end of the tree section
    file_contents.insert(offset, '---\n')
    offset += 1

    file_contents.insert(offset, DISK_BLOCKS + '\n')
    offset += 1

    # separator for end of the blocks section
    file_contents.insert(offset, '---\n')
    offset += 1

    # iterate on all nodes
    for node in PreOrderIter(root):
        # if it's a leaf node and file get
        if node.is_leaf and node.fileType == "f":
            path = get_file_path(node)

            # ----------[ Contiguous allocation ]----------
            if typeOfAllocation == 1:
                file_contents.insert(offset, path + " " + str(node.allocBlocks[0]) + " " + str(node.allocBlocks[1]) + '\n')
            # -----------[ Indexed allocation ]------------
            elif typeOfAllocation == 2:
                file_contents.insert(offset, path + " " + str(node.allocBlocks[0]) + '\n')
                offset += 1
                file_contents.insert(offset, ' '.join([str(x) for x in node.allocBlocks[1]]) + '\n')
            # ------------[ Linked allocation ]------------
            else:
                file_contents.insert(offset, path + " " + str(node.allocBlocks[0][0]) + " " + str(node.allocBlocks[-1][0]) + '\n')
                offset += 1
                file_contents.insert(offset, ' '.join(['-'.join(str(y) for y in x) for x in node.allocBlocks]) + '\n')

            offset += 1

    # separator for end of the allocation section
    file_contents.insert(offset, '###\n')
    offset += 1

    # writing the updates to the vfs file
    with open("DiskStructure.vfs", "w", encoding='utf-8') as f:
        file_contents = ''.join(file_contents)
        f.write(file_contents)


# holds all users
users = {}

# current user
current_user = "admin"


def load_all_users():
    global users
    with open("user.txt", "r", encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]

        for user_entry in lines:
            username = user_entry.split(',')[0]
            password = user_entry.split(',')[1]
            users[username] = password


def login(username, password):
    global current_user
    try:
        if users[username] == password:
            current_user = username
        else:
            print("Incorrect password!")
    except KeyError:
        print("Username doesn't exist!")


def main():
    # load users from user.txt file
    load_all_users()

    # Determine the type of allocation at first
    # to know the VFS file's structure
    allocation_type()

    # loading data from VFS file
    load_vfs_file()

    while True:
        cmd = input("%s:$ " % current_user)
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

        # ex: Login test pass
        elif cmd[0] == "Login":
            if len(cmd) == 3:
                login(cmd[1], cmd[2])
            else:
                print("Usage: Login <username> <password>")

        # ex: Login test pass
        elif cmd[0] == "TellUser":
            print(current_user)

        elif cmd[0] == "exit":
            break

        else:
            print("ERROR: Unknown command!")

    # saving data to VFS file
    save_vfs_file()


if __name__ == '__main__':
    main()
