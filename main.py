import os
import sys

import bisect

from formatter import Formatter


input_dir_name = "extracted_raw/"
output_dir_name = "extracted/"
if not os.path.exists(output_dir_name):
    os.mkdir(output_dir_name)


def line_sort_key(formatted_line: str) -> str:
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


def main():
    file_names = tuple([file_name for file_name in os.listdir(input_dir_name)])

    formatter = Formatter("", "")

    result_with_n = []
    result_without_n = []

    file_names = ["22KaTaKaCa.txt"]

    for file_name in file_names:
        print(f"Processing {input_dir_name}{file_name}")
        tag = "".join(file_name.split(".")[0].split())
        if tag[-1].isnumeric():
            tag = tag[:-1]
        with open(f"{input_dir_name}{file_name}") as f:
            lines = f.readlines()
            format = lines.pop(0)
            for line in lines:
                print(line)
                formatted_line = formatter.format(line)
                if r"{}" in formatted_line:
                    bisect.insort(result_without_n, formatted_line, key=line_sort_key)
                else:
                    result_with_n.append(formatted_line)
            # result = [formatter.format(line) + '\n' for line in lines]
            # result = []
            # for i, line in enumerate(lines):
            #     try:
            #         result.append(formatter.format(line) + "\n")
            #     except ValueError:
            #         print(f"N and P not found in file {file_name} on line {i}!")
    with open("marvel.dat", "w") as f:
        for line in result_without_n:
            f.write(line + "\n")


if __name__ == "__main__":
    main()
