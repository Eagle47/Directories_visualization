import os
import sys

import matplotlib.pyplot as plt
import numpy as np


def get_list_of_dirs(dir_name):
    l = []
    for x in os.listdir(dir_name):
        path = os.path.join(dir_name, x)
        if not os.path.islink(path):
            l.append(path)

    return l


def dir_size(dir_name):
    l = get_list_of_dirs(dir_name)

    s = 0
    for x in l:
        if os.path.isfile(x):
            s += os.path.getsize(x)

        if os.path.isdir(x):
            s += dir_size(x)

    return s


top_dir = os.path.abspath(sys.argv[1])
print('Top dir size: ', dir_size(top_dir) / 2**20, 'MB')

l_dirs = get_list_of_dirs(top_dir)
size_top_dir = dir_size(top_dir)

l_size = []
s = 0
for x in l_dirs:
    if os.path.isdir(x):
        l_tmp = []
        prev_dir_size = dir_size(x)
        l_dirs_tmp = get_list_of_dirs(x)

        for y in l_dirs_tmp:
            if os.path.isdir(y):
                tmp = dir_size(y)
                l_tmp.append(tmp / prev_dir_size)

        l_tmp.append((prev_dir_size - sum(l_tmp)) / prev_dir_size)
        l_size.append(l_tmp)

        s += dir_size(x)
l_size.append([(size_top_dir - s) / size_top_dir])

fig, ax = plt.subplots()

size = 0.3
vals = []
for x in l_size:
    vals.append(sum(x))

flattened = []
for i in l_size:
    for j in i:
        flattened.append(j)

ax.pie(vals, radius=1, wedgeprops=dict(width=size, edgecolor='w'))
ax.pie(flattened, radius=1 + size, wedgeprops=dict(width=size, edgecolor='w'))

plt.show()
