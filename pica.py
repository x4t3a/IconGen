#!/usr/bin/env python3
#


from PIL import Image, ImageDraw
import cgi
import io
import os
import random
import shutil
import sys
import const


def main():
    args = Args()
    if args.debug:
        args.sendDebug()
        return
    elif args.help:
        args.sendHelp()
        return
    body_color = args.body if args.body else getRandom(const.BODY_COLORS)
    img = generateImg(ImgProps('RGB', args.size, getRandom(const.BACK_COLORS), body_color))
    sendImg(img)
    return


class Args:
    def __init__(self):
        self.args = cgi.FieldStorage()
        self.size = (
            int(self.args[ 'size' ].value)
            if (('size' in self.args) and (self.args[ 'size' ].value.isdigit()) and
                (const.IMAGE_SIZE_MIN < int(self.args[ 'size' ].value) <= const.IMAGE_SIZE_MAX))
            else const.IMAGE_SIZE_DEF
        )
        self.debug = (
            True
            if ('debug' in self.args) and (self.args[ 'debug' ].value.lower() in ('yes', 'true', 'y', '1'))
            else False
        )
        self.help = (
            True
            if ('help' in self.args) and (self.args[ 'help' ].value.lower() in ('yes', 'true', 'y', '1')) and not self.debug
            else False
        )
        self.body = (
            self.args[ 'body' ].value
            if ('body' in self.args)
            else None
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
        sys.stdout.buffer.write(const.HELP_STRING)
        return


def sendString(*strings):
    for string in strings:
        attach = b'' if string == '\n' else b' '
        sys.stdout.buffer.write(string.encode('utf-8') + attach)
    return 


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


