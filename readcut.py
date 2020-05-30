from pprint import pprint

from align import align_read_stream

DOG_HEADER_SIZE = 20

def read_sin16be(f):
    return int.from_bytes(f.read(2), byteorder='big', signed=True)

def read_uin16be(f):
    return int.from_bytes(f.read(2), byteorder='big', signed=False)

def read_uin32be(f):
    return int.from_bytes(f.read(4), byteorder='big', signed=False)

def read_sin32be(f):
    return int.from_bytes(f.read(4), byteorder='big', signed=True)

def read_uint8(f):
    return f.read(1)[0]

def read_pstring(f):
    return f.read(read_uint8(f))

def get_line(data):
    align_read_stream(data, 2)
    return read_pstring(data)

def read_bank_header(data):
    tag = data.read(4).decode()
    assert tag == 'AmBk', tag
    bank_no = read_uin16be(data)
    bank_type = read_uin16be(data) # 0 for chip memory, 1 for fast memory
    bank_length = read_uin32be(data)
    bank_flags = bank_length & 0xf0000000
    bank_length &= 0x0fffffff
    bank_name = data.read(8).decode()
    assert data.tell() == DOG_HEADER_SIZE, data.tell()
    return tag, bank_no, bank_type, bank_flags, bank_length, bank_name

def get_lines(data, cmax):
    for _ in range(cmax):
        align_read_stream(data, 4)
        current_id = read_sin32be(data)
        yield current_id, read_pstring(data)

def parse_cut_file(data, encoding='cp862'):
    tag, bank_no, bank_type, bank_flags, bank_length, bank_name = read_bank_header(data)
    print(tag, bank_no, bank_type, bank_flags, bank_length, bank_name)


    

    pad = data.read()
    # assert set(pad) == {0}, pad

    print()
    print(len(pad) / 4)

    assert data.tell() == bank_length + 12, (data.tell(), bank_length + 12)


if __name__ == "__main__":
    import sys
    import glob

    if not len(sys.argv) > 1:
        print('Usage: readdog.py FILE1 [FILE2] ...')
        exit(1)
    target = sys.argv[1]
    for fname in glob.iglob(target):
        with open(fname, 'rb') as data:
            parse_cut_file(data, encoding='cp862')
