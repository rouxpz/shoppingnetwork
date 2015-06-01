import os
from os import system
import feedparser
from random import randrange
import urllib2
from bs4 import BeautifulSoup
import re
import glob
import threading

home_path = os.getcwd()
print home_path

def openPage(url):

	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	page = opener.open(url)
	soup = BeautifulSoup(page, from_encoding="utf-8")
	opener.close()
	return soup

def getImages(soup):

	path = 'csn_processing/data/'
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

def getFullDescription(soup):
	text = soup.find_all(id="postingbody")
	desc = str(text[0]).replace('<section id="postingbody">', '').replace('</section>', '').replace('<br/>', '').replace('"', ' inches').replace('&amp;', '&')
	return desc

def collectEntry():
	f = feedparser.parse("https://newyork.craigslist.org/search/sss?format=rss")

	select = randrange(len(f.entries))

	selection = f.entries[select]
	# print selection

	title = unicode.encode(selection.title, "utf-8")
	# summary = unicode.encode(selection.summary, "utf-8")

	title = title.split("&#x0024;")
	# summary = summary.lower()

	print(selection.id)
	raw = openPage(selection.id)
	getImages(raw)
	summary = getFullDescription(raw)

	print title
	# print summary

	with open('data.txt', 'wb') as file_:
		file_.write(title[0])
		file_.write('\n')
		file_.write(title[1])
		file_.write('\n')
		file_.write(summary)
		file_.close()

	os.chdir(home_path)
	print os.getcwd()

	startTimer()

def startTimer():
	print "starting timer..."
	t = threading.Timer(300.0, collectEntry)
	t.start()

collectEntry()
