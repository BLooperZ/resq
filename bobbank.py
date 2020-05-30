import sys
import glob
import os

import colorsys

from PIL import Image
import numpy as np

# N = 256
# RGB_tuples = [((x * 313 // 11) % 256, (x * 217 // 23) % 256, (x * 27 // 3) % 256) for x in range(N)]
# palt = [int(x) for sublist in RGB_tuples for x in sublist]
# print(palt)

def read_uin16le(f):
    return int.from_bytes(f.read(2), byteorder='little', signed=False)

def unpack(f):

    entries = read_uin16le(f)
    for i in range(entries):

        width = read_uin16le(f)
        height = read_uin16le(f)
        xhotspot = read_uin16le(f)
        yhotspot = read_uin16le(f)

        print(width, height, xhotspot, yhotspot)

        size = width * height

        data = f.read(size)
        assert len(data) == size
        yield (width, height, xhotspot, yhotspot), data

# def convert_to_pil_image(liner, width, height):
#     npp = np.array([ord(x) for x in liner], dtype=np.uint8)
#     npp.resize(height, width)
#     im = Image.fromarray(npp, mode='P')
#     return im

# def get_bg_color(row_size, f):
#     BGS = ['0', 'n']

#     def get_bg(idx):
#         return BGS[f(idx) % len(BGS)]
#     return get_bg

# def resize_pil_image(w, h, bg, im):
#     nbase = convert_to_pil_image(str(bg) * w * h, w, h)
#     # nbase.paste(im, box=itemgetter('x1', 'y1', 'x2', 'y2')(loc))
#     nbase.paste(im, box=(0,0))
#     return nbase

def get_pcx(basename):
    try:
        return Image.open(f'PCX/{basename[:-4]}.PCX')
    except:
        pass
    try:
        return Image.open(f'PCX/{basename[:-4].split("_")[0]}.PCX')
    except:
        pass
    try:
        return Image.open(f'PCX/{basename[:-4].split("_")[0][:-1]}.PCX')
    except:
        print('could not find matching PCX file')
        return None

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('Usage: bobbank.py path/to/extracted/game/BBK/*.BBK')
        print('checked with *.ACT, *.BBK, *.SAM')
        exit(1)
    pat = sys.argv[1]

    for fname in glob.glob(pat):
        basename = os.path.basename(fname)

        # w = 320
        # h = 200
        # grid_size = 16

        # enpp = np.array([[0] * w * grid_size] * h * grid_size, dtype=np.uint8)
        # bim = Image.fromarray(enpp, mode='P')

        # get_bg = get_bg_color(grid_size, lambda idx: idx + int(idx / grid_size))

        pcx = get_pcx(basename)

        os.makedirs('OUT', exist_ok=True)

        with open(fname, 'rb') as infile:
            for idx, (loc, data) in enumerate(unpack(infile)):
                width, height, *_ = loc
                npp = np.array([x for x in data], dtype=np.uint8).reshape((height, width))
                im = Image.fromarray(npp, mode='P')
                if pcx:
                    im.putpalette(pcx.palette)
                # im.putpalette(palt)
                im.save(f'OUT/{basename[:-4]}_{idx:03d}.png', transparency=0)

        #         im = resize_pil_image(w, h, get_bg(idx), im)
        #         bim.paste(im, box=((idx % grid_size) * w, int(idx / grid_size) * h))
        # bim.save(f'OUT/{basename}.png')
