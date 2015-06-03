import os
from os import system
import feedparser
from random import randrange
import urllib2
from bs4 import BeautifulSoup
import re
import glob
import threading

#to do:
#1 - extract email address
#2 - skip posts without photos
#3 - clean up any lingering HTML in the description

home_path = os.getcwd()

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

	if len(images) > 1:

		for i in images:
			if images.index(i) != 1:
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
	else:
		print "no images found"
		collectEntry()

def getFullDescription(soup):
	text = soup.find_all(id="postingbody")
	desc = str(text[0]).replace('<section id="postingbody">', '').replace('</section>', '').replace('<br/>', '').replace('"', ' inches').replace('&amp;', '&')
	return desc

def getContactInfo(_id):
	link = "http://newyork.craigslist.org/reply/nyc/for/" + _id
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	contact = opener.open(link)
	soup = BeautifulSoup(contact, from_encoding="utf-8")
	opener.close()

	email = soup.a.contents
	return email[0]

def collectEntry():
	os.chdir(home_path)
	print os.getcwd()

	f = feedparser.parse("https://newyork.craigslist.org/search/sss?format=rss")

	select = randrange(len(f.entries))

	selection = f.entries[select]
	# print selection

	title = unicode.encode(selection.title, "utf-8")
	link = unicode.encode(selection.link, "utf-8")

	if len(title) == 1:
		title.append("???")

	title = title.split("&#x0024;")
	title[0] = title[0].replace('&amp;', '&')
	# summary = summary.lower()

	r = re.findall(r'/[^/]*$', link)
	_id = r[0].replace('/', '').replace('.html', '')

	print _id
	email = getContactInfo(_id)
	print email

	print(selection.link)
	raw = openPage(selection.link)
	getImages(raw)
	summary = getFullDescription(raw)

	print title
	# print summary

	with open('data.txt', 'wb') as file_:
		file_.write(title[0])
		file_.write('\n')
		file_.write(title[1])
		file_.write('\n')
		file_.write(link)
		file_.write('\n')
		file_.write(email)
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
