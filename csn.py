import os
from os import system
import feedparser
from random import randrange
import urllib2
from bs4 import BeautifulSoup
import re
import glob
from Tkinter import *
from PIL import Image, ImageTk


def openPage(url):

	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	page = opener.open(url)
	soup = BeautifulSoup(page, from_encoding="utf-8")
	opener.close()
	return soup

def getImages(soup):

	path = 'data/'
	os.chdir(path)
	files = glob.glob('*.jpg')
	for f in files:
		os.unlink(f)

	counter = 0
	images = soup.find_all("img")

	for i in images:
		link = str(i.get("src"))
		link = link.replace("50x50c.jpg", "600x450.jpg")
		print link

		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
		photo = opener.open(link)

		with open(str(counter) + '.jpg', 'wb') as file_:
			file_.write(photo.read())
			file_.close()

		opener.close()

		counter += 1

f = feedparser.parse("https://newyork.craigslist.org/search/sss?format=rss")

select = randrange(len(f.entries))

selection = f.entries[select]
# print selection

title = unicode.encode(selection.title, "utf-8")
summary = unicode.encode(selection.summary, "utf-8")

title = title.split("&#x0024;")

print(selection.id)
raw = openPage(selection.id)
getImages(raw)

print title
print summary

canvas = Canvas(width=960, height=540, bg="black")
canvas.pack(expand = YES, fill = BOTH)

PILFile = Image.open('0.jpg')
photo = ImageTk.PhotoImage(PILFile)
label = Label(image=photo)
label.image = photo # keep a reference!

canvas.create_image(960/2, 540/2, image = photo)

mainloop()

# s = 'say ' + summary
# system(s)