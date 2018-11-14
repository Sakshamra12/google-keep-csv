#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, bs4, glob, unicodecsv as csv
from dateutil.parser import parse
from datetime import datetime

files = glob.glob("Keep/*.html")
notes = []

#Prep CSV file
now = datetime.now()
csvout = "notes_%s.csv" % now.strftime("%Y-%m-%d_%H%M")
writer = csv.writer(open(csvout, 'wb'))
writer.writerow(['date', 'title', 'content', 'file'])

for file in files:
	page = open(file)
	soup = bs4.BeautifulSoup(page.read(), "html.parser")

	#Make Excel-Friendly date
	googDate = soup.select('.heading')[0].getText().strip()
	xlDate = datetime.strftime(parse(googDate), '%m/%d/%Y %H:%M')

	content = soup.select(".content")[0].getText()
	content_has_checkboxes = content.find(u"☐") is not -1 or content.find(u"☑") is not -1
	# If the note has checkboxes, simply remove <br>
	if content.find(u"☐") is not -1 or content.find(u"☑") is not -1:
		# Convert <br>'s to line breaks.
		for br in soup.select('.content')[0].find_all("br"):
			br.replace_with("\n")
		content = soup.select(".content")[0].getText()
	else:
		# The previous method truncates other notes after the first \n. To avoid this issue, use Tag.strings
		content = "\n".join([s for s in soup.select(".content")[0].strings])
	try:
		note = {
			"date": xlDate,
			"title": soup.select('.title')[0].getText(),
			"content": content
		}
		writer.writerow([note['date'],note['title'],note['content'], file])
		print('[' + note['date'] + ']' + note['title'])

	#In case a note has a blank title or content, continue anyway
	except Exception as e:
		print("**NOTE** %s has blank title or content (%s)." % (file, e))
		pass

print('\n'+'-'*20 + '\nDone! %s notes saved to %s\n' % (len(files), csvout))