# EXTRACTED_FILE_NAME = "extracted.dat"
#
# with open(EXTRACTED_FILE_NAME) as f:
#     lines = f.readlines()


# upper v1 v2 v3
# lower v1 v2 v3
# upper j p s
# upper n
# lower j p s
# lower n
# upper j
# lower j
# upper e/f
# lower e/f


# def get_n(upper_v, lower_v, upper_jp, lower_jp, upper_e, lower_e) -> tuple[str, str]:
#     for line in lines:
#         splitted_line = tuple(line.split())
#         # print(type(splitted_line[:3]))
#         if upper_v == splitted_line[:3] and lower_v == splitted_line[3:6] and upper_jp == splitted_line[6:8] and lower_jp == splitted_line[9:11] and upper_e == splitted_line[-2] and lower_e == splitted_line[-1]:
#             return splitted_line[8], splitted_line[-3]
#     # raise ValueError("Not found")
#     return ("", "")
#
# def get_np(upper_v, lower_v, upper_j, lower_j, upper_e, lower_e) -> tuple[str, str, str, str]:
#     for line in lines:
#         splitted_line = tuple(line.split())
#         # print(type(splitted_line[:3]))
#         if upper_v == splitted_line[:3] and lower_v == splitted_line[3:6] and upper_j == splitted_line[6] and lower_j == splitted_line[9] and upper_e == splitted_line[-2] and lower_e == splitted_line[-1]:
#             return splitted_line[8], splitted_line[-3], splitted_line[7], splitted_line[10]
#     raise ValueError("Not found")
#     # return ("", "", "", "")
#
# def get_np_from_lower_n(upper_v, lower_v, upper_e, lower_e, lower_n) -> tuple[str, str, str]:
#     for line in lines:
#         splitted_line = tuple(line.split())
#         # print(type(splitted_line[:3]))
#         if upper_v == splitted_line[:3] and lower_v == splitted_line[3:6] and upper_e == splitted_line[-2] and lower_e == splitted_line[-1] and lower_n == splitted_line[-3]:
#             return splitted_line[8], splitted_line[7], splitted_line[10]
#     raise ValueError("Not found")
#     # return ("", "", "")


# file_name = "n2o.6iso.296K.1E-31.15Kcm-1.Y02-A8.dmsC.dat"
# file_name = "n2o.12iso.296K.1E-31.15Kcm-1.Y02-A8.dmsC.v2.dat"

# format j e/f # E v1 v2 l v3 useless u
file_name = "./extracted_j_l.dat"

# label = "42"

# with open(file_name) as f:
#     lines = [
#         " ".join(line.split()[5: 13] + line.split()[14: 17] + line.split()[18: 19] + line.split()[21:]) + '\n'
#         for line in f.readlines() if line.startswith(label)
#     ]
#
# with open(new_file_name, 'w') as f:
#     f.writelines(lines)

def get_p_from_line(line: str) -> str:
    splitted_line = line.split()
    v1, v2, v3 = [int(splitted_line[i]) for i in (4, 5, 7)]
    return str(2 * v1 + v2 + 4 * v3)


def get_l_from_line(line: str) -> str:
    return line.split()[6]


def line_key(line: str) -> str:
    return get_p_from_line(line) + " " + get_l_from_line(line)


def sort_key(line:str) -> float:
    return float(line.split()[3])


n_table: dict[str, list[str]] = {}

with open(file_name) as f:
    lines = f.readlines()

for line in lines:
    key = line_key(line)
    if key not in n_table:
        n_table[key] = [line]
    else:
        n_table[key].append(line)

for key in n_table.keys():
    n_table[key].sort(key=sort_key)

