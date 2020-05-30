import sys
import glob
import os

from PIL import Image
import numpy as np

def write_uin16le(number):
    return number.to_bytes(2, byteorder='little', signed=False)

def unpack(f):

    entries = read_uin16le(f)
    for i in range(entries):

        width = read_uin16le(f)
        height = read_uin16le(f)
        xhotspot = read_uin16le(f)
        yhotspot = read_uin16le(f)

        size = width * height

        data = f.read(size)
        assert len(data) == size
        yield (width, height, xhotspot, yhotspot), data

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
        print('Usage: bobbank.py I1.SAM')
        print('checked with *.ACT, *.BBK, *.SAM')
        exit(1)
    target = sys.argv[1]

    # HOTSPOTS FOR I1.SAM
    # hotspots = [
    #     (104, 110),
    #     (104, 110),
    #     (104, 110),
    #     (104, 110),
    #     (74, 99),
    #     (74, 99),
    #     (74, 99),
    #     (74, 99),
    #     (54, 99),
    #     (54, 99),
    #     (54, 99),
    #     (54, 99),
    #     (100, 102),
    #     (100, 102),
    #     (100, 102),
    #     (100, 102)
    # ]

    # HOTSPOTS FOR C9.BBK
    hotspots = [
        (80, 73),
        (80, 73),
        (80, 73),
        (160, 93)
    ]

    files = os.listdir('IN')

    files = list(fname for fname in files if fname.split('_')[0] == target[:-4])

    with open(target, 'wb') as output_file:
        output_file.write(write_uin16le(len(files)))

        for fname, (xhs, yhs) in zip(files, hotspots):
            im = Image.open(f'IN/{fname}')
            npp = (np.asarray(im) + (np.asarray(im) != 0)).tolist()
            # for row in npp:
            #     print(row)
            # break
            output_file.write(write_uin16le(len(npp[0])))
            output_file.write(write_uin16le(len(npp)))
            output_file.write(write_uin16le(xhs))
            output_file.write(write_uin16le(yhs))
            output_file.write(bytes([item for sublist in npp for item in sublist]))

    # with open(fname, 'rb') as infile:
    #     for idx, (loc, data) in enumerate(unpack(infile)):
    #         width, height, *_ = loc
    #         npp = np.array([x for x in data], dtype=np.uint8).reshape((height, width))
    #         im = Image.fromarray(npp, mode='P')
    #         if pcx:
    #             im.putpalette(pcx.palette)
    #         im.save(f'OUT/{basename[:-4]}_{idx:03d}.png')
