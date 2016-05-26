#!/usr/bin/env python3
#


from PIL import Image, ImageDraw
import cgi
import io
import os
import random
import shutil
import sys


def main():
    args = Args()
    if args.debug:
        args.sendDebug()
        return
    elif args.help:
        args.sendHelp()
        return
    img = generateImg(ImgProps('RGB', args.size, getRandom(BACK_COLORS), getRandom(BODY_COLORS)))
    sendImg(img)
    return


class Args:
    def __init__(self):
        self.args = cgi.FieldStorage()
        self.size = (
            int(self.args[ 'size' ].value)
            if ('size' in self.args) and (int(self.args[ 'size' ].value) > 50) and (self.args[ 'size' ].value.isdigit())
            else 500
        )
        self.debug = (
            True
            if ('debug' in self.args) and (self.args[ 'debug' ].value.lower() in ('yes', 'true', 't', '1'))
            else False
        )
        self.help = (
            True
            if ('help' in self.args) and (self.args[ 'help' ].value.lower() in ('yes', 'true', 't', '1')) and not self.debug
            else False
        )
        return


    def sendDebug(self):
        d = vars(self)
        members = [attr for attr in d if not callable(attr) and not attr.startswith("__")]
        sys.stdout.buffer.write(b'Content-Type: text/plain\n\n')
        sys.stdout.buffer.write(b'  ** Vars **\n')
        for member in members:
            if member == 'args': continue
            sendString(str(member), str(d[ member ]), '\n')
        sys.stdout.buffer.write(b'\n\n  ** Actual get arguments **\n')
        for key in self.args.keys():
            sendString(key, self.args[ key ].value, '\n')
        return


    def sendHelp(self):
        help_string = (
            b'Content-Type: text/plain\n\n'
            b'  ** Help **\n'
            b'size (>=50, default = 500)'
        )
        sys.stdout.buffer.write(help_string)
        return


def sendString(*strings):
    for string in strings:
        attach = b'' if string == '\n' else b' '
        sys.stdout.buffer.write(string.encode('utf-8') + attach)
    return 


BACK_COLORS = [
    (247, 202, 201), # Rose Quartz
    (247, 120, 107), # Peach Echo
    (145, 168, 208), # Serenity
    (  3,  79, 132), # Snorkel Blue
    (249, 231,  42), # Buttercup
    (152, 221, 222), # Limpet Shell
    (152, 150, 164), # Lilac Gray
    (220,  68,  58), # Fiesta
    (177, 143, 106), # Iced Coffee
    (121, 199,  83), # Green Flash
]


BODY_COLORS = [
    'aqua', 'azure', 'black', 'brown', 'red', 'blue', 'green', 'cyan',
]


def getRandom(lst):
    return random.choice(lst)


def sendImg(img):
    sys.stdout.buffer.write(b'Content-Type: image/png\n\n')
    shutil.copyfileobj(img, sys.stdout.buffer)
    return


def ImgPath(rel_path):
    return os.path.abspath(rel_path)


class ImgProps:
    def __init__(self, im_kind = 'RGB', im_size = 500, im_back = (255, 255, 0), im_body = 'black'):
        self.kind = im_kind # 'RGB'
        self.size = im_size # 500
        self.back = im_back # (255, 255, 0)
        self.body = im_body
        return


def generateImg(props):
    img = Image.new(props.kind, (props.size, props.size), props.back)
    drw = ImageDraw.Draw(img)
    img_map = generateImgMap()
    rect_size = int(props.size / 10)
    rect_start = (int(props.size / 5), int(props.size / 5))
    rect_end = sumTuples(rect_start, (rect_size, rect_size))
    for r in img_map:
        rect_start = (rect_start[ 0 ], int(props.size / 5))
        rect_end = sumTuples(rect_start, (rect_size, rect_size))
        for c in r:
            if c:
                drw.rectangle((rect_start, rect_end), fill = props.body)
            rect_start = sumTuples(rect_start, (0, rect_size))
            rect_end = sumTuples(rect_start, (rect_size, rect_size))
        rect_start = sumTuples(rect_start, (rect_size, 0))
        rect_end = sumTuples(rect_start, (rect_size, rect_size))
    buf = io.BytesIO()
    imgn = img.rotate(90) # well >.>
    imgn.save(buf, 'PNG')
    buf.seek(0)
    return buf


def sumTuples(l, r):
    return tuple(map(sum, zip(l, r)))


def generateImgMap():
    img_map = [ [ False ] * 6 for i in range(0, 6) ]
    flen = len(img_map)
    hlen = int(flen / 2)
    for i in range(0, flen):
        for j in range(0, hlen):
            t = True if random.randint(0, 100) < 40 else False
            img_map[ i ][ j ] = t
    for i in range(0, flen): 
        shift = 2
        for j in range(hlen, flen): 
            img_map[ i ][ j ] = img_map[ i ][ shift ]
            shift -= 1
    return img_map


if '__main__' in __name__:
    main()


