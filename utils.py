import sys
from PIL import Image


def transparent(img, color):
    bgcolor = (color[0], color[1], color[2], 255)
    width, height = img.size
    img = img.convert('RGBA')

    pix = img.load()

    for w in xrange(width):
        for h in xrange(height):
            if pix[w, h] == bgcolor:
                pix[w, h] = (255, 255, 255, 0)

    img.format = 'png'
    return img


def crop(img, size):
    for i in xrange(wrange):
        for j in xrange(hrange):
            image = get_crop(img, size, (i, j))
            image.save('i-j.%s' % img.format)


def get_crop(img, size, xy):
    w, h = size
    width, height = img.size
    x, y = xy

    wrange = width // w
    hrange = height // h

    return img.crop((x, y, x+w, y+h))
