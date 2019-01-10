import pprint

array_size = int(input("Please Enter Array Size:"))

array = []
for i in range(array_size):
    array.append([])
    for j in range(array_size):
        array[i].append(0)


def print_array():
    # print(array)
    pprint.pprint(array)


def move_check():
    if cmd == "w" and x == 0:
        print(" ********** Out of MAP! **********")
        print_array()
        return 0
    elif cmd == "s" and x == array_size-1:
        print(" ********** Out of MAP! **********")
        print_array()
        return 0
    elif cmd == "a" and y == 0:
        print(" ********** Out of MAP! **********")
        print_array()
        return 0
    elif cmd == "d" and y == array_size-1:
        print(" ********** Out of MAP! **********")
        print_array()
        return 0
    else:
        return 1


array[0][0] = 1

print_array()


x = 0
y = 0
while 1:
    cmd = input("Command:")
    if cmd == "w" and move_check() == 1:
        x -= 1
        array[x][y] = 1
        print_array()
    elif cmd == "a" and move_check() == 1:
        y -= 1
        array[x][y] = 1
        print_array()
    elif cmd == "d" and move_check() == 1:
        y += 1
        array[x][y] = 1
        print_array()
    elif cmd == "s" and move_check() == 1:
        x += 1
        array[x][y] = 1
        print_array()
