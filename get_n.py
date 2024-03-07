EXTRACTED_FILE_NAME = "extracted.dat"

with open(EXTRACTED_FILE_NAME) as f:
    lines = f.readlines()


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


def get_n(upper_v, lower_v, upper_jp, lower_jp, upper_e, lower_e) -> tuple[str, str]:
    for line in lines:
        splitted_line = tuple(line.split())
        # print(type(splitted_line[:3]))
        if upper_v == splitted_line[:3] and lower_v == splitted_line[3:6] and upper_jp == splitted_line[6:8] and lower_jp == splitted_line[9:11] and upper_e == splitted_line[-2] and lower_e == splitted_line[-1]:
            return splitted_line[8], splitted_line[-3]
    # raise ValueError("Not found")
    return ("", "")

def get_np(upper_v, lower_v, upper_j, lower_j, upper_e, lower_e) -> tuple[str, str, str, str]:
    for line in lines:
        splitted_line = tuple(line.split())
        # print(type(splitted_line[:3]))
        if upper_v == splitted_line[:3] and lower_v == splitted_line[3:6] and upper_j == splitted_line[6] and lower_j == splitted_line[9] and upper_e == splitted_line[-2] and lower_e == splitted_line[-1]:
            return splitted_line[8], splitted_line[-3], splitted_line[7], splitted_line[10]
    raise ValueError("Not found")
    # return ("", "", "", "")

def get_np_from_lower_n(upper_v, lower_v, upper_e, lower_e, lower_n) -> tuple[str, str, str]:
    for line in lines:
        splitted_line = tuple(line.split())
        # print(type(splitted_line[:3]))
        if upper_v == splitted_line[:3] and lower_v == splitted_line[3:6] and upper_e == splitted_line[-2] and lower_e == splitted_line[-1] and lower_n == splitted_line[-3]:
            return splitted_line[8], splitted_line[7], splitted_line[10]
    raise ValueError("Not found")
    # return ("", "", "")
