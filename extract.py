
import os
import sys

def read_uint16be(f):
    return int.from_bytes(f.read(2), byteorder='big', signed=False)

def read_uint32be(f):
    return int.from_bytes(f.read(4), byteorder='big', signed=False)

def extract_index(f):
    tag = read_uint32be(f)
    version = f.read(7).decode().rstrip('\0')
    compression = read_uint16be(f)
    # version = f.read(13)
    entries = read_uint16be(f)
    for i in range(entries):
        name = f.read(12).decode().rstrip('\0')
        bundle = f.read(1)
        offset = read_uint32be(f)
        size = read_uint32be(f)
        yield name, bundle, offset, size


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('usage: extract.py FILE')
        exit(1)

    fname = sys.argv[1]
    with open(fname, 'rb') as queen_file:
        index = list(extract_index(queen_file))
        for name, bundle, offset, size in index:
            print(name, bundle, offset, size)
            assert queen_file.tell() == offset
            # queen_file.seek(offset, 0)
            with open(f'OUT/{name}', 'wb') as output:
                output.write(queen_file.read(size))

	# _resourceEntries = file->readUint16BE();
	# _resourceTable = new ResourceEntry[_resourceEntries];
	# for (uint16 i = 0; i < _resourceEntries; ++i) {
	# 	ResourceEntry *re = &_resourceTable[i];
	# 	file->read(re->filename, 12);
	# 	re->filename[12] = '\0';
	# 	re->bundle = file->readByte();
	# 	re->offset = file->readUint32BE();
	# 	re->size = file->readUint32BE();
	# }