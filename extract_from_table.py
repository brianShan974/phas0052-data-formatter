# file_name = "n2o.6iso.296K.1E-31.15Kcm-1.Y02-A8.dmsC.dat"
file_name = "n2o.12iso.296K.1E-31.15Kcm-1.Y02-A8.dmsC.v2.dat"
new_file_name = "extracted.dat"
label = "42"

with open(file_name) as f:
    lines = [
        " ".join(line.split()[5: 13] + line.split()[14: 17] + line.split()[18: 19] + line.split()[21:]) + '\n'
        for line in f.readlines() if line.startswith(label)
    ]

with open(new_file_name, 'w') as f:
    f.writelines(lines)
