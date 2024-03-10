# format j e/f # E v1 v2 l v3 useless u
file_name = "./fort.1900.N2O.456.20211108"

# new_file_name = "extracted.dat"
new_file_name = "extracted_j_l_sorted_by_energy.dat"


def is_valid(line: str) -> bool:
    splitted_line = line.split()
    return splitted_line[0] == splitted_line[6]


def get_p_from_line(line: str) -> str:
    splitted_line = line.split()
    v1, v2, v3 = [int(splitted_line[i]) for i in (4, 5, 7)]
    return str(2 * v1 + v2 + 4 * v3)


def get_l_from_line(line: str) -> str:
    return line.split()[6]


def line_key_pl(line: str) -> str:
    return get_p_from_line(line) + " " + get_l_from_line(line)


def line_key_full(line: str) -> str:
    splitted_line = line.split()
    v1, v2, v3, l = [int(splitted_line[i]) for i in (4, 5, 7, 6)]
    return f"{v1} {v2} {v3} {l}"


def sort_key(line: str) -> float:
    return float(line.split()[3])


def main():
    with open(file_name) as f:
        lines = [
            " ".join(line.strip().split()) for line in f.readlines() if is_valid(line)
        ]

    temp_table: dict[str, list[str]] = {}
    lowest_lines: list[str] = []

    table: dict[str, list[str]] = {}

    for line in lines:
        key = line_key_full(line)
        if key not in temp_table:
            temp_table[key] = [line]
        else:
            temp_table[key].append(line)

    for key in temp_table.keys():
        temp_table[key].sort(key=sort_key)
        lowest_line = temp_table[key][0]
        lowest_lines.append(lowest_line)

    for line in lowest_lines:
        key = line_key_pl(line)
        if key not in table:
            table[key] = [line]
        else:
            table[key].append(line)

    for key in table.keys():
        table[key].sort(key=sort_key)
        for i, line in enumerate(table[key]):
            table[key][i] = table[key][i] + " " + str(i + 1) + "\n"

    with open(new_file_name, "w") as f:
        for value in table.values():
            f.writelines(value)


if __name__ == "__main__":
    main()
