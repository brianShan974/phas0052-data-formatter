import os
import sys

from formatter import Formatter


input_dir_name = "extracted_raw/"
output_dir_name = "extracted/"
if not os.path.exists(output_dir_name):
    os.mkdir(output_dir_name)


def write_to_file(tag, lines):
    if os.path.exists(f"{tag}.txt"):
        mode = 'a'
    else:
        mode = 'w'
    with open(f"{tag}.txt", mode) as f:
        f.writelines(lines)


def main():
    file_names = tuple([file_name for file_name in os.listdir(input_dir_name)])

    formatter = Formatter("", "")

    for file_name in file_names:
        print(f"Processing {input_dir_name}{file_name}")
        tag = "".join(file_name.split('.')[0].split())
        if tag[-1].isnumeric():
            tag = tag[:-1]
        with open(f"{input_dir_name}{file_name}") as f:
            lines = f.readlines()
            format = lines.pop(0)
            formatter.reset(format, tag)
            # result = [formatter.format(line) + '\n' for line in lines]
            result = []
            for i, line in enumerate(lines):
                try:
                    result.append(formatter.format(line) + '\n')
                except ValueError:
                    print(f"N and P not found in file {file_name} on line {i}!")
            write_to_file(f"{output_dir_name}{tag}", result)

if __name__ == "__main__":
    main()
