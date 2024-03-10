import os
from typing import Literal


from formatter import Formatter


input_dir_name = "extracted_raw/"
output_dir_name = "extracted/"
if not os.path.exists(output_dir_name):
    os.mkdir(output_dir_name)


def lower_state_sort_key(formatted_line: str) -> str:
    indices = (-6, -5, -3)
    splitted_line = formatted_line.split()
    return " ".join([splitted_line[index] for index in indices])


def write_to_file(tag, lines):
    if os.path.exists(f"{tag}.txt"):
        mode = "a"
    else:
        mode = "w"
    with open(f"{tag}.txt", mode) as f:
        f.writelines(lines)


def n_sort_key(formatted_line: str) -> float:
    return float(formatted_line.split()[0])


def get_base_n(formatted_line: str) -> Literal[1, 2]:
    return 1 if formatted_line.split()[-3] == 'e' else 2


def get_tag(formatted_line: str) -> str:
    return formatted_line.split()[-1]


def transition_sort_key(formatted_line: str) -> str:
    indices = (2, 3, 5, -6, -5, -3)
    splitted_line = formatted_line.split()
    return " ".join([splitted_line[index] for index in indices])


def tag_sort_key(formatted_line: str) -> str:
    return get_tag(formatted_line) + ' ' + transition_sort_key(formatted_line)


def find_n(lines_without_n: dict[str, list[str]]) -> list[str]:
    for key in lines_without_n.keys():
        lines_without_n[key].sort(key=n_sort_key)
        base_n = get_base_n(lines_without_n[key][0])
        for (i, line) in enumerate(lines_without_n[key]):
            lines_without_n[key][i] = lines_without_n[key][i].format(i + base_n)
    result = []
    for value in lines_without_n.values():
        result.extend(value)
    return result


# I found this code at https://codereview.stackexchange.com/questions/182733/base-26-letters-and-base-10-using-recursion
def base10ToBase26Letter(num):
    ''' Converts any positive integer to Base26(letters only) with no 0th 
    case. Useful for applications such as spreadsheet columns to determine which 
    Letterset goes with a positive integer.
    '''
    if num <= 0:
        return ""
    elif num <= 26:
        return chr(96+num)
    else:
        return base10ToBase26Letter(int((num-1)/26))+chr(97+(num-1)%26)


def tag_lines_by_source_and_transitions(lines_with_n: list[str]) -> list[str]:
    dict_for_tagging: dict[str, list[str]] = {}
    for line in lines_with_n:
        key = tag_sort_key(line)
        if key not in dict_for_tagging:
            dict_for_tagging[key] = [line]
        else:
            dict_for_tagging[key].append(line)
    for key in dict_for_tagging.keys():
        pass
    return []


def main():
    file_names = tuple([file_name for file_name in os.listdir(input_dir_name)])

    formatter = Formatter("", "")

    lines_with_n = []
    lines_without_n = {}

    # file_names = ["22KaTaKaCa.txt"]

    for file_name in file_names:
        print(f"Processing {input_dir_name}{file_name}")
        tag = "".join(file_name.split(".")[0].split())
        if tag[-1].isnumeric():
            tag = tag[:-1]
        with open(f"{input_dir_name}{file_name}") as f:
            lines = f.readlines()
            format = lines.pop(0)
            formatter.reset(format, tag)
            for line in lines:
                print(f"{line = }")
                try:
                    formatted_line = formatter.format(line)
                except AssertionError:
                    continue
                if r"{}" in formatted_line:
                    key = lower_state_sort_key(formatted_line)
                    if key not in lines_without_n:
                        lines_without_n[key] = [formatted_line]
                    else:
                        lines_without_n[key].append(formatted_line)
                else:
                    lines_with_n.append(formatted_line)
            # result = [formatter.format(line) + '\n' for line in lines]
            # result = []
            # for i, line in enumerate(lines):
            #     try:
            #         result.append(formatter.format(line) + "\n")
            #     except ValueError:
            #         print(f"N and P not found in file {file_name} on line {i}!")
            for _ in range(5):
                print()
    lines_with_n.extend(find_n(lines_without_n))
    with open("marvel.dat", "w") as f:
        for line in lines_with_n:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
