#!/usr/bin/env python
#coding=utf-8

import argparse
from PIL import Image
from PIL import ImageDraw
import os

def watermark(args):
    if not os.path.exists("./watermark_dest"):
        os.system("mkdir watermark_dest")

    color = args["color"]
    word = args["w"]
    save,show = args["save"], args["show"]
    x,y  = int(args["x"]), int(args["y"])

    fileName,dirName = None, None
    if not args["f"] and not args["d"]:
        dirName = "."
    elif args["f"]:
        fileName = args["f"]
    else:
        dirName = args["d"]
    if fileName:
        im = Image.open(fileName).convert("RGBA")
        mark(im,word,x,y,color,save,show)
    else:
        for imname in os.listdir(dirName):
            try:
                im = Image.open(dirName +  "/" + imname).convert("RGBA")
                mark(im,word,x,y,color,save,show)
            except:
                pass

def masic(args):
    if not os.path.exists("./masic_dest"):
        os.system("mkdir masic_dest")
    im = Image.open(args["f"])
    fileName = im.filename
    im = im.convert("RGBA")
    pixel = im.load()
    save,show = args["save"], args["show"]
    xpos,ypos,width,height = int(args["x"]),int(args["y"]),int(args["width"]),int(args["height"])
    for x in range(xpos, xpos+width):
        for y in range(ypos, ypos+height):
            rp,gp,bp,op = 0,0,0,0
            for i in range(9):
                for j in range(9):
                    rp += pixel[x+i-4, y+j-4][0]
                    gp += pixel[x+i-4, y+j-4][1]
                    bp += pixel[x+i-4, y+j-4][2]
                    op += pixel[x+i-4, y+j-4][3]
            pixel[x,y] = (rp/81,gp/81,bp/81,op/81)
    if show:
        im.show()
    if save:
        im.save('./masic_dest/' + fileName.split('/')[-1])


def cut(args):
    if not os.path.exists("./cut_dest"):
        os.system("mkdir cut_dest")
    save,show = args["save"], args["show"]
    xpos,ypos,width,height = int(args["x"]),int(args["y"]),int(args["width"]),int(args["height"])

    box = (xpos,ypos,width+xpos,height+ypos)
    im = Image.open(args["f"])
    print box
    if xpos < 0 or ypos <0 or xpos + width >= im.size[0] or height+ypos >= im.size[1]:
        print "the size of this image is {}, please set a valid area inside the image".format(im.size)
        exit()
    newIm = im.crop(box)
    if show:
        newIm.show()
    if save:
        newIm.save('./cut_dest/' + im.filename.split('/')[-1])


def resize(args):
    save,show = args["save"], args["show"]
    if not os.path.exists("./resize_dest"):
        os.system("mkdir resize_dest")
    im = Image.open(args["f"])
    filename = im.filename
    if args["width"]:
        width = int(args["width"])
        per = (width / float(im.size[0]))
        height = int(im.size[1] * per)
        im = im.resize((width,height))
    elif args["height"]:
        height = int(args["height"])
        per = (height / float(im.size[1]))
        weight = int(im.size[0] * per)
        im = im.resize((width,height))
    if show:
        im.show()
    if save:
        im.save('./resize_dest/' + filename.split('/')[-1])

def mark(im, mark,x,y,color,save=True,show=False):
    draw = ImageDraw.Draw(im)
    def getColor(s):
        return {
            "white": (255,255,255),
            "red": (255,0,0),
            "green": (0,255,0),
            "blue": (0,0,255),
            "black": (0,0,0)
        }.get(s, (255,255,255))
    draw.text((x,y),mark,getColor(color))
    if show:
        im.show()
    if save:
        im.save("./watermark_dest/" + im.filename.split('/')[-1])





parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="subparser_name")

wmParser = subparsers.add_parser('watermark',help="add watermark in an image")
wmParser.add_argument("--f", help="the file need to be processed")
wmParser.add_argument("--d", help="the directory of images need to be processed")
wmParser.add_argument("--x", default=0,help="the x-pos of watermark")
wmParser.add_argument("--y", default=0,help="the y-pos of watermark")
wmParser.add_argument("--w", default=os.getenv("LOGNAME"), help="the word of the watermark")
wmParser.add_argument("--show", action="store_true", help="show the result" )
wmParser.add_argument("--save", action="store_true", help="save the result")
wmParser.add_argument("--color", default="white",help="specify the color of the watermark", choices=['white','red','blue','green','black'])

masicParser = subparsers.add_parser('masic', help="add cover in an image")
masicParser.add_argument("--f", help="the file need to be processed")
masicParser.add_argument("--x",required=True,type=int)
masicParser.add_argument("--y",required=True,type=int)
masicParser.add_argument("--width",required=True,type=int)
masicParser.add_argument("--height",required=True,type=int)
masicParser.add_argument("--show", action="store_true", help="show the result" )
masicParser.add_argument("--save", action="store_true", help="save the result")


cutParser = subparsers.add_parser('cut', help="cut an image")
cutParser.add_argument("--f", help="the file need to be processed", required=True)
cutParser.add_argument("--x",required=True,type=int)
cutParser.add_argument("--y",required=True,type=int)
cutParser.add_argument("--width",required=True,type=int)
cutParser.add_argument("--height",required=True,type=int)
cutParser.add_argument("--show", action="store_true", help="show the result" )
cutParser.add_argument("--save", action="store_true", help="save the result")

resizeParser = subparsers.add_parser('resize', help="resize an image")
resizeParser.add_argument("--f", required=True, help="the width of the processed image")
resizeParser.add_argument("--width", type=int, help="the width of the processed image")
resizeParser.add_argument("--height", type=int, help="the height of the processed image")
resizeParser.add_argument("--show", action="store_true", help="show the result" )
resizeParser.add_argument("--save", action="store_true", help="save the result")

args =  vars(parser.parse_args())

if args['subparser_name'] == 'watermark':
    watermark(args)

if args['subparser_name'] == 'masic':
    masic(args)

if args['subparser_name'] == 'cut':
    cut(args)

if args['subparser_name'] == "resize":
    resize(args)
