from PIL import Image
import numpy as np

def get_font_bytes(fname):
	w = 10
	h = 10

	bim = Image.open(fname)

	for row in range(16):
		for col in range(16):
			area = (col * w, row * h, (col + 1) * w, (row + 1) * h)
			im = bim.crop(area)
			im = list(np.asarray(im.crop((0,0,8,8))))

			yield [int(''.join(chr(x) for x in line).replace('@', '1').replace('_', '0'), 2) for line in im]


if __name__ == '__main__':

	with open('QUEEN.EXE', 'r+b') as executable:

		pre = executable.read(248715)
		executable.seek(256 * 8, 1)

		post = executable.read()

		executable.seek(0, 0)
		
		executable.write(pre)
		for frame in get_font_bytes('FONTS/font_he_new.png'):
			print(', '.join(f'0x{c:02X}' for c in frame) + ',')
			executable.write(bytes(frame))
		executable.write(post)


