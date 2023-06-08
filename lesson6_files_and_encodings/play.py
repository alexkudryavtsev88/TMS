from pathlib import Path

root = Path(__file__).parent

# r+ mode: raises Error if file not found by the specified path!
with open(root.joinpath("my_file.txt"), 'r+') as rw_file:
    print("Working in 'r+' mode!")

    print("Read file 1:\n" + repr(rw_file.read()))
    rw_file.write("LINE4\n")

    # need to move cursor at the begin of the file otherwise the second 'read' call doesn't return anything
    # (file content Iterator will be exhausted after the first 'read' call)
    rw_file.seek(0)
    print("Read file 2:\n" + repr(rw_file.read()))

    rw_file.write("LINE5\n")
    rw_file.seek(0)
    print("Read file 3:\n" + repr(rw_file.read()))

print()

# w+ mode: erases the existing file content when opens it!
# with open(root.joinpath("my_file.txt"), 'w+') as rw_file:
#     print("Read file 1:\n" + repr(rw_file.read()))
#     rw_file.write("LINE6\n")
#
#     # need to move cursor at the begin of the file otherwise the second 'read' call doesn't return anything
#     # (file content Iterator will be exhausted after the first 'read' call)
#     rw_file.seek(0)
#     print("Read file 2:\n" + repr(rw_file.read()))
#
#     rw_file.write("LINE7\n")
#     rw_file.seek(0)
#     print("Read file 3:\n" + repr(rw_file.read()))

print()

# r+ mode: raises Error if file not found by the specified path!
with open(root.joinpath("my_file.txt"), 'a+') as rw_file:
    print("Working in 'r+' mode!")

    rw_file.seek(0)  # need to make seek(0) before the first reading!
    print("Read file 1:\n" + repr(rw_file.read()))
    rw_file.write("LINE4\n")

    # need to move cursor at the begin of the file otherwise the second 'read' call doesn't return anything
    # (file content Iterator will be exhausted after the first 'read' call)
    rw_file.seek(0)
    print("Read file 2:\n" + repr(rw_file.read()))

    rw_file.write("LINE5\n")
    rw_file.seek(0)
    print("Read file 3:\n" + repr(rw_file.read()))