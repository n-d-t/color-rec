from PIL import Image
import numpy

y = 0; x = 0

def decColor(x):
    b = x % 256; x = x / 256;
    g = x % 256; x = x / 256;
    r = x % 256; x = x / 256;
    return (r, g, b)

def gen_img(x, y):
    data = numpy.zeros((y, x, 3),dtype=numpy.uint8)
    return data
    
def paint(img, y1, x1, y2, x2, color):
    for i in xrange(y1, y2):
        for j in xrange(x1, x2):
            img[i][j] = color
    return img

def perm(s, n):
	c = []
	for x in s:
		c.append([x])
	for l in range(2, n+1):
		c_i = []
		for i in c:
			for x in s:
				k = i + [x]
				c_i.append(k)
		
		c = c_i
	return c

img_data = gen_img(256,256)
for r in range(0,255):
    for b in range(0,255):
        img_data[r+(0*255)][b] = (r,b,145);

"""

for i in range(0, 16777216):
    color = decColor(i)
    if(x == 1000):
        x = 0; y = y + 1
    
    img_data[y][x] = color
    x = x + 1
"""

im = Image.fromarray(img_data)
im.save("your_file6.jpeg")