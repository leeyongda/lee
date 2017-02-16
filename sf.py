# coding=utf-8

from random import randrange

l = [randrange(10000) for i in range(1000)]
print 42 in l

s = set(l)
print 42 in s


def s(seq, i=0):
    if i == len(seq):
        return 0
    return s(req, i + 1) + seq[i]


def gnomesort(seq):
    i = 0
    while i < len(seq):
        if i == 0 or seq[i - 1] <= seq[i]:
            i += 1
        else:
            seq[i], seq[i - 1] = seq[i - 1], seq[i]
            i -= 1

gnomesort([1, 2, 5, 4, 0])

seq = [randrange(10**10) for i in range(100)]
dd = float("inf")
for x in seq:
    for y in seq:
        if x == y:
            continue
        d = abs(x - y)
        if d < dd:
            xx, yy, dd = x, y, d
print xx, yy

seq.sort()
dd = float("inf")


def sel_sort(req, i):
    if i == 0:
        return
    max_j = i
    for j in range(i):
        if req[j] > req[max_j]:
            max_j = j

    req[i], req[max_j] = req[max_j], req[i]
    sel_sort(req, i)


# def sel_sort_rec(req, i):
#     for i in range（len(seq) - 1, 0, - 1):
#         max_j=i
#         for j in range(i):
#             if req[j] > req[max_j]:
#                 max_j=j
#         req[i], req[max_j]=req[max_j], req[i]


import bcrypt
s = 'aa'
hash = bcrypt.hashpw(s, bcrypt.gensalt())
print hash
