#!/usr/bin/env python3
import os
import itertools
from operator import itemgetter

filetype = 'CUT'

def read_lines(lines):
    for idx, line in enumerate(lines):
        fname, num, text = line.split('\t')
        text = text.replace('`', '"')
        yield fname, f'{int(num):03d} {text}'

with open('fixed.txt', 'r', encoding='utf-8') as ff:
    lines = list(read_lines(ff))
    for fname, texts in itertools.groupby(lines, key=itemgetter(0)):
        with open(f'FIXED-CUT/{fname}', 'w', encoding='cp862') as output:
            output.write(f'Original {filetype} file: {fname[:-4]}.{filetype}\n\n')
            output.writelines(text for _, text in texts)
    # # print(f'{filename}\t{line}')
    # print(text + '\n')
    # # print(filename + '\n')
