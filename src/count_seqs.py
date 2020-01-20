import os


def count_seqs(file):
    res = 0
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if len(line) > 0:
            if line[0] == '>':
                res += 1
    return res


dir = "/Users/martagomes/Desktop/CaseStudy/kos_no_orgs/"
files = os.listdir(dir)

total = 0
for file in os.listdir(dir):
    total += count_seqs(os.path.join(dir, file))

print(total)
