# format j e/f # E v1 v2 l v3 useless u
file_name = "./fort.1900.N2O.456.20211108"

# new_file_name = "extracted.dat"
new_file_name = "extracted_j_l.dat"


def is_valid(line: str) -> bool:
    splitted_line = line.split()
    return splitted_line[0] == splitted_line[6]


with open(file_name) as f:
    lines = [line for line in f.readlines() if is_valid(line)]

with open(new_file_name, 'w') as f:
    f.writelines(lines)
