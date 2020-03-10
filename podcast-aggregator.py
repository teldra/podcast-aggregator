#!/bin/python3

import podcastparser
import urllib
import requests
import hashlib
import sys
from datetime import datetime
# include standard modules
import argparse

# initiate the parser
parser = argparse.ArgumentParser()
# add long and short argument
parser.add_argument("--title", "-t", help="feed title")
parser.add_argument("--link", "-l", help="feed link")
parser.add_argument("--image", "-i", help="feed image")

# read arguments from the command line
args, unknown = parser.parse_known_args()

print("<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\">")
print("<channel>")
print("<title>%s</title>" % (args.title))
print("<link>%s</link>" % (args.link))
print("<image>")
print("<url>%s</url>" % (args.image))
print("</image>")
print("\n")

for i in range(len(unknown)):
	if i != 0:
		feedurl = unknown[i]
		feed = podcastparser.parse(feedurl, urllib.request.urlopen(feedurl), max_episodes=7)
		feedtitle = feed.get('title', '')
		feedlink = feed.get('link', '')
		feeddesc = feed.get('description', '')
		for ep in feed['episodes']:
			eptitle = ep['title']
			epdesc = ep['description']
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
