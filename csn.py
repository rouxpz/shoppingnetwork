import os
from os import system
import feedparser
from random import randrange
import urllib2
from bs4 import BeautifulSoup
import re
import glob
from Tkinter import *


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


root = Tk()

photo = PhotoImage(file='0.jpg')
canvas = Canvas(width=1920/2, height=1080/2)
canvas.create_image(0, 0, image = photo)

root.mainloop()

# s = 'say ' + summary
# system(s)

print title
print summary