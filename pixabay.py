import requests
from bs4 import BeautifulSoup
from PIL import Image
import imageio
import numpy as np
from PIL import ImageFont
from PIL import ImageDraw
import textwrap
import csv
import random


def get_picture_link(WebUrl,pageNum):
 f = open("pixabay.csv", "a+")
 for pageNo in range(pageNum):
    url = WebUrl+ repr(pageNo)
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    for link in s.select(".search_results > .item > a > img"):
        src_string = link.get("src")
        if(src_string != "/static/img/blank.gif"):
            link = src_string
            print(link)
            f.write(src_string+"\n")
        else:
            link = link.get("data-lazy")
            print(link)
            f.write(link+"\n")


def edit_image(imageName,gradient_magnitude=0.5):
    # load image
    im = Image.open(imageName)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    width, height = im.size  # Get dimensions
    # resize image if too small
    if(1102 > height):
     ratio = 1102.0/height
     width = width*ratio
     width = int(width)
     im = im.resize((int(width), 1102), Image.ANTIALIAS)

    left = (width - 735) / 2
    top = 0
    right = (width + 735) / 2
    bottom = 1102

    im = im.crop((left, top, right, bottom))

    # put black layer on image
    overlay_color = img_est_blackwhite(imageName)
    print(overlay_color)
    overlay = Image.open("pic/"+overlay_color)
    overlay = overlay.convert("RGBA")
    overlay_rate = 0.4
    if(overlay_color == "white.png"):
        overlay_rate = 0.2
    new_img = Image.blend(im, overlay, overlay_rate)
    new_img = new_img.convert('RGB')
    new_img.save(imageName, "JPEG")


def img_est_blackwhite(img):
    f = imageio.imread(img, as_gray=True)
    is_light = np.mean(f) > 127
    return 'black.png' if is_light else 'white.png'

def write_quote(img,text,pic_name):
    draw = ImageDraw.Draw(img)
    font_list = ["font/Aleo-Regular.otf","font/Antonio-Regular.ttf","font/LeagueGothic-Regular.otf","font/Satisfy-Regular.ttf"]

    font = ImageFont.truetype(font_list[random.randint(0,3)], 72)
    y_text = 200
    lines = textwrap.wrap(text, width=22)
    if len(text) < 80:
        y_text = 300

    for line in lines:
        width, height = font.getsize(line)
        draw.text(((735 - width) / 2, y_text), line,(255,255,255), font=font)
        y_text += height
    img.save(pic_name)

def download_picture(pic_link,newname):
    r = requests.get(pic_link)

    with open(newname, 'wb') as f:
        f.write(r.content)


def load_quotes():
    with open('quotes.csv', 'r') as csvfile:
        quotesreader = csv.reader(csvfile, delimiter='\r')
        return list(quotesreader)


def load_pic():
    with open('pixabay.csv', 'r') as csvfile:
        picreader = csv.reader(csvfile, delimiter='\r')
        for row in picreader:
            return list(picreader)

def main():
    #load quotes
    quotes = load_quotes()
    quotes_list_no = random.sample(range(0, 267), 200)
    #load pic
    pics = load_pic()
    pics_list_no = random.sample(range(0, 64790), 200)
    for x in range(100):
        current_pic = pics[pics_list_no[x]][0]
        current_quote = quotes[quotes_list_no[x]][0]
        current_name = "pic/template_"+repr(x)+".jpg"
        download_picture(current_pic,current_name)
        edit_image(current_name)
        img = Image.open(current_name)
        write_quote(img,current_quote,current_name)
        print("done 2")

main()