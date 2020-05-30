#!/usr/bin/env python3
import re
import os
for filename in sorted(os.listdir('DOG-TMFs')):
    with open(f'DOG-TMFs/{filename}', 'r', encoding='cp862') as ff:
        for idx, line in enumerate(ff):
            if idx > 1:
                num, *others = line.split(' ')
                text = ' '.join(others)
                text = text[:-1]
                text = text.replace('"', '`')
                lines = re.split(r'(?=\*.{2})', text)
                lines = (l[::-1] for l in lines)
                text = '"' + '\n'.join(lines) + '"'
                # print(f'{filename}\t{line}')
                print(text + '\n')
                # print(filename + '\n')
