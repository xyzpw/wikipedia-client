#!/usr/bin/env python3

import requests
import argparse
import json
import re
import datetime
import pydoc
from src import _fetchHtmlText
from src import _loadingBar
from src import _fetchRelated
from src import _returnErrors

USER_AGENT = "xyzpw/wikipedia-client"

parser = argparse.ArgumentParser()
parser.add_argument("--title", help="title of wikipedia page", metavar="<title>")
parser.add_argument("--related", help="displays topics related to the current wiki page", action="store_true")
parser.add_argument("--infobox", help="displays the infobox portion of page alone", action="store_true")
parser.add_argument("--pager", help="displays wiki page in paginated format", action="store_true")
parser.add_argument("--fullpage", help="displays full html page", action="store_true")
args = vars(parser.parse_args())

usingFullPage, usingPaginatedFormat = args.get("fullpage"), args.get("pager")
usingRelated, usingInfoBox = args.get("related"), args.get("infobox")

if usingRelated and usingFullPage:
    raise SystemExit("'related' and 'fullpage' parameters cannot be active simultaneously")
if usingInfoBox and (usingFullPage or usingRelated):
    raise SystemExit("'fullpage' or 'related' cannot be used with 'infobox'")

if usingFullPage:
    loadingbar = _loadingBar.MyLoadingBar(0, 8, 4)
elif usingInfoBox:
    loadingbar = _loadingBar.MyLoadingBar(0, 9, 3)
else:
    loadingbar = _loadingBar.MyLoadingBar(0, 20, 5)

def print_loadingProgress(msg, end='\r'):
    print(f"\x1b[2K{msg}: {loadingbar.__str__()}", end=end)

wiki_title = args.get("title")

if wiki_title is None:
    wiki_title = input("wiki title: ")

if usingInfoBox:
    if usingRelated:
        raise SystemExit("'related' parameter cannot be used with 'infobox'")
    print_loadingProgress("requesting html")
    htmlApiCall = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{wiki_title}", headers={"user-agent": USER_AGENT})
    loadingbar.incrementProgress()
    if htmlApiCall.status_code != 200:
        print("\n", end='')
        error_response = _returnErrors.getErrorDetails(htmlApiCall.text)
        raise SystemExit(f"error loading wikipedia page: '{error_response}'")
    print_loadingProgress("converting html to full-page text")
    wikiTextFromHtml = _fetchHtmlText.htmlToWikiText(htmlApiCall.text, USER_AGENT)
    loadingbar.incrementProgress()
    fullPageText = _fetchHtmlText.html2txt(wikiTextFromHtml)
    wiki_page = ""
    print_loadingProgress("creating infobox")
    for line in fullPageText.splitlines():
        if line.startswith("|"):
            wiki_page += line + "\n"
    loadingbar.complete()
    print_loadingProgress("wikipedia page finished loading successfully", end='\n')
    if usingPaginatedFormat:
        pydoc.pager(wiki_page)
        raise SystemExit(0)
    else:
        print(wiki_page)
        raise SystemExit(0)

if usingFullPage:
    try:
        print_loadingProgress("requesting html")
        htmlApiCall = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/html/{wiki_title}", headers={"user-agent": USER_AGENT})
        if htmlApiCall.status_code != 200:
            print("\n", end='')
            error_response = _returnErrors.getErrorDetails(htmlApiCall.text)
            raise SystemExit(f"error loading wikipedia page: '{error_response}'")
        loadingbar.incrementProgress()
        print_loadingProgress("converting html to full-page text")
        wikiTextFromHtml = _fetchHtmlText.htmlToWikiText(htmlApiCall.text, USER_AGENT)
        fullPageText = _fetchHtmlText.html2txt(wikiTextFromHtml)
        loadingbar.incrementProgress()
        loadingbar.complete()
    except KeyboardInterrupt:
        raise SystemExit(0)
    except Exception as ERROR:
        if loadingbar.progress != 0:
            print("\n", end='')
        raise SystemExit(ERROR)
    print_loadingProgress("wikipedia page finished loading successfully", end='\n')
    if usingPaginatedFormat:
        pydoc.pager(fullPageText)
        raise SystemExit(0)
    else:
        print(fullPageText)
        raise SystemExit(0)

print_loadingProgress("requesting page summary")
summaryApiCall = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_title}", headers={"user-agent": USER_AGENT})
wikipedia_summary = json.loads(summaryApiCall.text)
loadingbar.incrementProgress()

print_loadingProgress("verifying response")
if summaryApiCall.status_code != 200:
    error_response = _returnErrors.getErrorDetails(summaryApiCall.text)
    print("\n", end='')
    raise SystemExit(f"error loading wikipedia page: '{error_response}'")
loadingbar.incrementProgress()

def print_bold(txt, end="\n"):
    print("\x1b[1m{}\x1b[0m".format(txt), end=end)

print_loadingProgress("creating browser-styled timestamp")
regex_timestamp = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d+)T(?:(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+))Z",
    wikipedia_summary.get("timestamp")
)
improved_timestamp = datetime.datetime(
    int(regex_timestamp.group("year")),
    int(regex_timestamp.group("month")),
    int(regex_timestamp.group("day")),
    int(regex_timestamp.group("hour")),
    int(regex_timestamp.group("minute")),
    int(regex_timestamp.group("second"))
).strftime(r"%-d %B, %Y, at %H:%M (UTC).")
loadingbar.incrementProgress()
# re-named keys for improved readability
wikipedia_info = {
    "title": str(wikipedia_summary.get("title")),
    "title_bold": "\x1b[1m" + str(wikipedia_summary.get("title")) + "\x1b[0m",
    "brief_description": str(wikipedia_summary.get("description")),
    "description": str(wikipedia_summary.get("extract")),
    "last_edited": improved_timestamp,
}

print_loadingProgress("creating wikipedia page")
wiki_page = ""
if wiki_title != wikipedia_info.get("title"):
    wiki_page += f"(Redirected from {wiki_title})\n\n"

if usingPaginatedFormat:
    wiki_page += wikipedia_info.get("title") + "\n\n"
else:
    wiki_page += wikipedia_info.get("title_bold") + "\n\n"
wiki_page += wikipedia_info.get("brief_description") + "\n\n"
wiki_page += wikipedia_info.get("description") + "\n\n"
if usingRelated:
    related_json = _fetchRelated.getPages(wikipedia_info["title"], USER_AGENT)
    wiki_page += "\nRelated Topics:\n---------------"
    lastTopicLength = 0
    for topic, description in related_json.items():
        wiki_page += "\n* {} - {}".format(topic, description)
        lastTopicLength = len(str(topic)) + len(str(description)) + 5
    wiki_page += "\n{}\n".format('-'*lastTopicLength)

wiki_page += f"\n\nThis page was last edited on {improved_timestamp}"
loadingbar.complete()
print_loadingProgress("wikipedia page loaded successfully", end='\n')

if usingPaginatedFormat:
    pydoc.pager(wiki_page)
    raise SystemExit(0)
else:
    print(wiki_page)
    raise SystemExit(0)
