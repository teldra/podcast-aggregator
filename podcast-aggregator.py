#!/bin/python3

import podcastparser
import urllib
import requests
import hashlib
import sys
from datetime import datetime

if len (sys.argv) <= 1 :
	print("Usage: python $URL ")
	sys.exit (1)

print("<rss xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">")
print("<channel>")
print("<title></title>")
print("<link></link>")

for i in range(len(sys.argv)):
	if i != 0:
		feedurl = sys.argv[i]
		feed = podcastparser.parse(feedurl, urllib.request.urlopen(feedurl), max_episodes=7)
		feedtitle = feed.get('title', '')
		feedlink = feed.get('link', '')
		feeddesc = feed.get('description', '')
		for ep in feed['episodes']:
			eptitle = ep['title']
			epdesc = ep['description']
			epdesc2 = ep['description'].encode('utf-8')
			eppubdate = datetime.utcfromtimestamp(int(ep['published'])).strftime('%a, %d %b %Y %T')
			enclosure = ep['enclosures'][0]
			epurl = enclosure['url'].split("?")[0]

print("<item>")
print("<title>%s: %s</title>" % (feedtitle.replace('&', '&amp;'),eptitle.replace('&', '&amp;')))
print("<description><![CDATA[%s\n\n%s\n\n<a href=\"%s\">%s</a>\n\n<a href=\"%s\">%s</a>\n]]></description>" % (epdesc, feeddesc, epurl, epurl, feedlink, feedlink))
print("<guid>%s</guid>" % (epurl))
print("<pubDate>%s UTC</pubDate>" % (eppubdate))
print("<enclosure url=\"%s\"/>" % (epurl))
print("</item>")
print("\n")

print("</channel>")
print("</rss>")
