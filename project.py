import timeit
import random


def prefix_function(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


print("Input length of substring")
k = int(input())
print("Input multiply of string")
h = int(input())
# генерация
# строки(1) - начало
s_string = ""
for i in range(k):
    num = random.randint(1, 1000000000)
    s_string += str(ord('a') + num % 26)
    # s_string += 'a'
main_string = ""
for i in range(k * h):
    num = random.randint(1, 1000000000)
    tt = num % h
    if tt == 0:
        main_string += s_string
    else:
        main_string += str(ord('a') + num % 26)
    # main_string += 'a'
# (1) - конец
print("Length of main string", len(main_string))
start_time = timeit.default_timer()
# find(2) - начало
res = 0
tr = 0
while 1:
    tr = main_string.find(s_string, tr)
    if tr == -1:
        break
    tr += 1
    res += 1
print("Number of find", res)
search_time = timeit.default_timer() - start_time
print("Time work:", search_time)
# (2) - конец
# (3) - префикс
# функция(КМП) - начало
print("KMP")
start_time = timeit.default_timer()
tmp = s_string + '#' + main_string
p = prefix_function(tmp)
res1 = 0
for i in range(len(p)):
    if p[i] == len(s_string):
        res1 += 1
print("Number of find", res1)
search_time = timeit.default_timer() - start_time
print("Time work:", search_time)
# (3) - конец
# (4) - Полимиальный
# хеш - начало
start_time = timeit.default_timer()
print("Hash")
x, m = 31, 10000007
n, kq = len(main_string), len(s_string)
pow1 = [0] * (n + 1)
pow1[0] = 1
for i in range(1, n + 1):
    pow1[i] = (pow1[i - 1] * x) % m
hash1 = [0] * (n + 1)
hash1[0] = 0
for i in range(1, n + 1):
    hash1[i] = (hash1[i - 1] + ((ord(main_string[i - 1]) - ord('a') + 1) * pow1[i - 1])) % m
s_hash = 0
for i in range(kq):
    s_hash = (s_hash + (ord(s_string[i]) - ord('a') + 1) * pow1[i]) % m
res2 = 0
for i in range(n - kq + 1):
    cur = hash1[i + kq]
    q = ((s_hash * pow1[i]) % m + hash1[i]) % m
    if cur == q:
        res2 += 1
print("Number of find", res2)
search_time = timeit.default_timer() - start_time
print("Time work:", search_time)
# (4) - конец
