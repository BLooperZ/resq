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

def parse_dog_file(data, encoding='cp862'):
    tag, bank_no, bank_type, bank_flags, bank_length, bank_name = read_bank_header(data)

    level_max = read_sin16be(data)
    skippable = level_max < 0
    level_max = abs(level_max)

    unique_key = read_sin16be(data)
    talk_key = read_sin16be(data)
    jmax = read_sin16be(data)
    pmax = read_sin16be(data)

    more = [{
        'game_state': read_sin16be(data),
        'test_value': read_sin16be(data),
        'item_number': read_sin16be(data)
    } for i in range(2)]

    pprint(more, sort_dicts=False)

    _person1_off = read_sin16be(data)
    _cutaway_off = read_sin16be(data)
    _person2_off = read_sin16be(data)
    _joe_off = 32 + level_max * 96

    _unk = read_uin32be(data)
    print('_unk', _unk)

    assert data.tell() == 32 + DOG_HEADER_SIZE, data.tell()

    dialogue = [[{
        'head': read_sin32be(data),
        'dialogueNodeValue1': read_sin32be(data),
        'gameStateIndex': read_sin32be(data),
        'gameStateValue': read_sin32be(data)
    } for i in range(6)] for i in range(level_max)]

    pprint(dialogue, sort_dicts=False)

    assert data.tell() == _joe_off + DOG_HEADER_SIZE

    print()
    print("## Joe's sentences")
    # Joe's sentences
    for current_id, line in get_lines(data, jmax):
        print(f'{current_id:04X}' if current_id else 'SSSS', line.decode(encoding))

    align_read_stream(data, 4)

    assert data.tell() == _person1_off + DOG_HEADER_SIZE, (data.tell(), _person1_off + DOG_HEADER_SIZE)

    print()
    print("## Other's sentences")
    # Other's sentences
    for current_id, line in get_lines(data, pmax):
        print(f'{current_id:04X}' if current_id else 'SSSS', line.decode(encoding))


    align_read_stream(data, 4)

    assert data.tell() == _cutaway_off + DOG_HEADER_SIZE, (data.tell(), _cutaway_off + DOG_HEADER_SIZE)


    print()
    print("## Cutaway")
    ca_state = read_sin16be(data)
    ca_test = read_sin16be(data)
    line = get_line(data)
    print(line.decode(encoding))

    align_read_stream(data, 4)

    assert data.tell() == _person2_off + DOG_HEADER_SIZE, (data.tell(), _person2_off + DOG_HEADER_SIZE)

    print()
    print("## Other's greeting")
    # Other's greeting
    line = get_line(data)
    print('XXXX', line.decode(encoding))

    print()
    print("## Joe's second greeting")
    # Joe's second greeting
    line = get_line(data)
    print('XXXX', line.decode(encoding))

    pad = data.read()
    assert set(pad) == {0}, pad

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
            parse_dog_file(data, encoding='cp862')
