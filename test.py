import csv
import json
from sys import stdin
from collections import defaultdict

file_name = input()
transl = defaultdict(str)
with open(file_name, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for i, row in enumerate(reader):
        if i == 0:
            continue
        transl[row[2]] = row[1]
csvfile.close()
ans = defaultdict(str)
data = list(map(str.strip, stdin))
for i, row in enumerate(data):
    cur = ""
    for j in range(0, len(row) - 1, 2):
        temp = row[j] + row[j + 1]
        if transl.get(temp, "non") == "non":
            cur += temp
        else:
            cur += transl[temp]
        cur += " "
    ans[i] = cur[:len(cur) - 1]
with open('tabula_rasa.json', 'w', encoding="utf-8") as f:
    json.dump(ans, f)
f.close()