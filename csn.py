import os
from os import system
import time
import shutil
import feedparser
from random import randrange
import urllib2
from bs4 import BeautifulSoup
import re
import glob
import threading

#to do:
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

	counter = 0
	images = soup.find_all("img")

	if len(images) > 1:

		path = 'csn_processing/tempStorage/'
		os.chdir(path)
		files = glob.glob('*.jpg')
		for f in files:
			os.unlink(f)

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

				time.sleep(15)

				print "moving on"

		return len(images)

	else:
		print "no images found"
		return 0

	os.chdir(home_path)

def getFullDescription(soup):
	text = soup.find_all(id="postingbody")
	desc = str(text[0]).replace('<section id="postingbody">', '').replace('</section>', '').replace('<br/>', '').replace('<br>', '').replace('"', ' inches').replace('&amp;', '&')
	contactLink = re.findall(r'<a(.*)a>', desc)

	if len(contactLink) > 0:
		desc = desc.replace(contactLink[0], '').replace('<a', '').replace('a>', '')

	return desc

def getContactInfo(_id):
	link = "http://newyork.craigslist.org/reply/nyc/for/" + _id
	soup = openPage(link)

	try:
		email = soup.a.contents
		return email[0]
	except AttributeError:
		print "no email"
		return "None"

def collectEntry():

	os.chdir(home_path)
	print os.getcwd()

	f = feedparser.parse("https://newyork.craigslist.org/search/sss?format=rss")

	select = randrange(len(f.entries))

	selection = f.entries[select]
	# print selection

	title = unicode.encode(selection.title, "utf-8")
	link = unicode.encode(selection.link, "utf-8")

	title = title.split("&#x0024;")

	if len(title) == 1:
		title.append("???")

	title[0] = title[0].replace('&amp;', '&')
	# summary = summary.lower()

	r = re.findall(r'/[^/]*$', link)
	_id = r[0].replace('/', '').replace('.html', '')

	print _id
	email = getContactInfo(_id)
	print email

	print(selection.link)
	raw = openPage(selection.link)
	photos = getImages(raw)
	summary = getFullDescription(raw)

	print title
	# print summary

	if email == "None" or photos == 0:
		print "starting over"
		os.chdir(home_path)
		print os.getcwd()
		startTimer(30.0)
	
	else:

		tempPath = home_path + '/csn_processing/tempStorage/'
		realPath = home_path + '/csn_processing/data/'

		os.chdir(realPath)
		oldFiles = glob.glob('*.jpg')
		for o in oldFiles:
			os.unlink(o)

		os.chdir(tempPath)

		files = glob.glob('*.jpg')

		for f in files:
			shutil.copy2(f, realPath + f)
		
		os.chdir(realPath)
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

		startTimer(180.0)

def startTimer(time):
	print "starting timer..."
	t = threading.Timer(time, collectEntry)
	t.start()

collectEntry()
