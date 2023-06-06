import json
from pathlib import Path

# encodings
my_string = "test"
my_byte_string = my_string.encode(encoding="utf-8")
assert my_byte_string == b'test'
emoji = "🙁"
print(emoji)
emoji_encoded_utf = emoji.encode(encoding="utf-8")
print(emoji_encoded_utf)
print(type(emoji_encoded_utf))
emoji_decoded_utf = emoji_encoded_utf.decode(encoding="utf-8")
assert emoji_decoded_utf == emoji

# work with Path
current_path = Path(__file__)  # get path to current file
current_dir = current_path.parent  # get path to current file's dir
print(current_dir)
current_file_name = current_path.stem  # file name without extension
print(current_file_name)

# find ALL python files in user space
for file in Path("/home").rglob("*.py"):
    print(file)

# work with Files
file = open(
    current_dir.joinpath("my_file.txt"),
    mode="r",
    encoding="utf-8"
)
file.close()  # always need to close the opened File

# Alternative: open the Files using Context manager
with open(
    current_dir.joinpath("my_file.txt"),
    mode="r",  # open the File in "read" mode
    encoding="utf-8"
) as my_file:
    # read ALL lines from file: lines will contain '\n' at the end
    rfile_lines = my_file.readlines()
    print(rfile_lines)

# using opened File object as Iterator
with open(
    current_dir.joinpath("my_file.txt"),
    mode="r",  # open the File in "read" mode
    encoding="utf-8"
) as my_file:
    for line in my_file:
        print(line.rstrip("\n"))
    # Iterator is exhausted here!

# write File
with open(
    current_dir.joinpath("my_file_out.txt"),
    mode="w",  # if File by this path is NOT exist - it will be created anyway
    encoding="utf-8"
) as write_file:
    new_data = [
        line.rstrip('\n') + '!\n' for line in rfile_lines
    ]
    write_file.writelines(new_data)

# work with JSON files:
my_dict = {"1": 2, "2": {"3": 4, "4": {"5": 5}}}
with open(
    current_dir.joinpath("my_json_file.json"),
    mode="w"
) as w_file:
    json.dump(my_dict, w_file, indent=4)

with open(
    current_dir.joinpath("my_json_file.json"),
    mode="r"
) as r_file:
    data = json.load(r_file)

    assert data == my_dict









