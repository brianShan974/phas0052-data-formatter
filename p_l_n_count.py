FILE_NAME = "./extracted/08NiSoPeTaLiWaHu_extracted.txt"

pln_dict: dict[str, int] = {}

with open(FILE_NAME) as f:
    for line in f.readlines():
        splitted_line = line.split()
        key = " ".join(splitted_line[2:5])
        if key in pln_dict:
            pln_dict[key] += 1
        else:
            pln_dict[key] = 1

print(len(pln_dict))
print(pln_dict.keys())
