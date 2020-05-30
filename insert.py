
import os
import sys

def read_uint16be(f):
    return int.from_bytes(f.read(2), byteorder='big', signed=False)

def read_uint32be(f):
    return int.from_bytes(f.read(4), byteorder='big', signed=False)

def write_uint16be(num):
    return num.to_bytes(2, byteorder='big', signed=False)

def write_uint32be(num):
    return num.to_bytes(4, byteorder='big', signed=False)

def extract_index(f):
    # tag = read_uint32be(f)
    # version = f.read(7).decode().rstrip('\0')
    # compression = read_uint16be(f)
    # # version = f.read(13)
    entries = read_uint16be(f)
    for i in range(entries):
        name = f.read(12)
        bundle = f.read(1)
        offset = read_uint32be(f)
        size = read_uint32be(f)
        yield name, bundle, offset, size


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print('usage: insert.py SOURCE_QUEEN.1c')
        exit(1)

    fname = sys.argv[1]

    out_idx = b''
    out_data = b''
    off_err = 0

    with open(fname, 'rb') as queen_file:
        with open(f'queen-new.1c', 'wb') as output:
            output.write(queen_file.read(13))
            index = list(extract_index(queen_file))
            entries = len(index)
            out_idx += write_uint16be(entries)
            data_offset = 15 + entries * 21
            for name, bundle, offset, size in index:
                assert offset + off_err == data_offset, (offset, data_offset)
                out_idx += name
                in_size = size
                stripped_name = name.decode().rstrip('\0')
                if os.path.exists(f'IN/{stripped_name}'):
                    with open(f'IN/{stripped_name}', 'rb') as insert_file:
                        out_data += insert_file.read()
                        in_size = insert_file.tell()
                        off_err += in_size - size
                else:
                    queen_file.seek(offset, 0)
                    out_data += queen_file.read(size)
                out_idx += bundle + write_uint32be(data_offset) + write_uint32be(in_size)
                queen_file.seek(offset, 0)
                data_offset += in_size
            output.write(out_idx)
            output.write(out_data)

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