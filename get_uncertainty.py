uncertainty_table: dict[str, str] = {}


with open("uncertainty_table.txt") as f:
    for line in f:
        key, value = line.split()
        uncertainty_table[key] = value


def get_uncert(tag: str) -> str:
    return uncertainty_table[tag]
