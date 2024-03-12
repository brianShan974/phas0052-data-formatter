# import sys
import os
from typing import Literal


from formatter import Formatter


INPUT_DIR_NAME = "extracted_raw/"
OUTPUT_DIR_NAME = "extracted/"
TARGET_FILE_NAME = "marvel.txt"
if not os.path.exists(OUTPUT_DIR_NAME):
    os.mkdir(OUTPUT_DIR_NAME)


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
    return 1 if formatted_line.split()[-3] == "e" else 2


def get_tag(formatted_line: str) -> str:
    return formatted_line.split()[-1]


def transition_sort_key(formatted_line: str) -> str:
    indices = (2, 3, 5, -6, -5, -3)
    splitted_line = formatted_line.split()
    return " ".join([splitted_line[index] for index in indices])


def tag_sort_key(formatted_line: str) -> str:
    return get_tag(formatted_line) + " " + transition_sort_key(formatted_line)


# def find_n(lines_without_n: dict[str, list[str]]) -> list[str]:
#     for key in lines_without_n.keys():
#         lines_without_n[key].sort(key=n_sort_key)
#         base_n = get_base_n(lines_without_n[key][0])
#         for i, line in enumerate(lines_without_n[key]):
#             lines_without_n[key][i] = lines_without_n[key][i].format(i + base_n)
#
#     result = []
#     for value in lines_without_n.values():
#         result.extend(value)
#     return result


# I found this code at https://codereview.stackexchange.com/questions/182733/base-26-letters-and-base-10-using-recursion
def base10ToBase25Letter(num):
    """Converts any positive integer to Base26(letters only) with no 0th
    case. Useful for applications such as spreadsheet columns to determine which
    Letterset goes with a positive integer.
    """
    if num <= 0:
        return ""
    elif num <= 25:
        return chr(65 + num)
    else:
        return base10ToBase25Letter(int((num - 1) / 25)) + chr(65 + (num - 1) % 25)


def tag_lines_by_source_and_transitions(lines_with_n: list[str]) -> list[str]:
    dict_for_tagging: dict[str, list[str]] = {}
    for line in lines_with_n:
        key = tag_sort_key(line)
        if key not in dict_for_tagging:
            dict_for_tagging[key] = [line]
        else:
            dict_for_tagging[key].append(line)
    for i, key in enumerate(dict_for_tagging.keys()):
        letter_index = base10ToBase25Letter(i + 1)
        for j, line in enumerate(dict_for_tagging[key]):
            dict_for_tagging[key][j] = (
                dict_for_tagging[key][j] + f".{letter_index}{str(j + 1)}"
            )

    result = []
    for value in dict_for_tagging.values():
        result.extend(value)
    return result


def main():
    file_names = tuple([file_name for file_name in os.listdir(INPUT_DIR_NAME)])

    formatter = Formatter("", "")

    lines = []

    # not_found_count = 0

    # file_names = ["22KaTaKaCa.txt"]

    for file_name in file_names:
        print(f"Processing {INPUT_DIR_NAME}{file_name}")
        tag = "".join(file_name.split(".")[0].split())
        if tag[-1].isnumeric():
            tag = tag[:-1]
        with open(f"{INPUT_DIR_NAME}{file_name}") as f:
            temp_lines = f.readlines()
            format = temp_lines.pop(0)
            formatter.reset(format, tag)
            for line in temp_lines:
                print(f"{line = }")
                try:
                    formatted_line = formatter.format(line)
                    lines.append(formatted_line)
                except AssertionError:
                    continue
                # except KeyError:
                #     not_found_count += 1
                #     continue
            # result = [formatter.format(line) + '\n' for line in lines]
            # result = []
            # for i, line in enumerate(lines):
            #     try:
            #         result.append(formatter.format(line) + "\n")
            #     except ValueError:
            #         print(f"N and P not found in file {file_name} on line {i}!")
            for _ in range(5):
                print()
    tagged_lines = tag_lines_by_source_and_transitions(lines)
    tagged_lines.sort(key=lower_state_sort_key)
    with open(TARGET_FILE_NAME, "w") as f:
        for line in tagged_lines:
            f.write(line + "\n")

    # print(f"{not_found_count = }")


if __name__ == "__main__":
    main()
