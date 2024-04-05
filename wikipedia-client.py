#!/usr/bin/env python3

import requests
import argparse
import json
import re
import datetime
import pydoc
from src import _loadingBar
from src import _fetchRelated
from src import _returnErrors
from src import _arghandler
from src import _findInPage
from src import _contentItemsHandler
from src import _wikipageBuilder
from src import _cleantextHandler
from src import _prettifyPage
from src.configHandler import *

USER_AGENT = "cloned from xyzpw/wikipedia-client.git"

parser = argparse.ArgumentParser()
parser.add_argument("--title", help="title of wikipedia page", metavar="<title>")
parser.add_argument("--related", help="displays topics related to the current wiki page", action="store_true")
parser.add_argument("--infobox", help="displays the infobox portion of page alone", action="store_true")
parser.add_argument("--pager", help="displays wiki page in paginated format", action="store_true")
parser.add_argument("--fullpage", help="displays full html page", action="store_true")
parser.add_argument("--find", help="displays each line that contains this text", metavar="<text>")
parser.add_argument("--no_highlight", help="disables highlighting of the find in page matches", action="store_true")
parser.add_argument("--contents", help="displays the content for a specified content section", metavar="<name>")
parser.add_argument("--content_items", help="displays the list of content items for the specified wiki page", action="store_true")
parser.add_argument("--no_prettify", help="disables prettifying text", action="store_true")
parser.add_argument("--no_hatnotes", help="removes hatnotes from the displayed text", action="store_true")
parser.add_argument("--no_cites", help="removes cites from the displayed text", action="store_true")
args = vars(parser.parse_args())
_arghandler.validateArgs(args)
args = readConfig(dict(args))

isCleanDisplay = args.get("no_hatnotes") or args.get("no_cites")

usingFullPage, usingPaginatedFormat = args.get("fullpage"), args.get("pager")
usingRelated, usingInfoBox = args.get("related"), args.get("infobox")
isSearchingForText = args.get("find") != None
isPretty = True if not args.get("no_prettify") else False

loadingbar = _loadingBar.MyLoadingBar(0, 20, 5)

def print_loadingProgress(msg, end='\r'):
    print(f"\x1b[2K{msg}: {loadingbar.__str__()}", end=end)

wiki_title = args.get("title")

if wiki_title == None:
    try:
        wiki_title = input("wiki title: ")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)

if args.get("content_items"):
    print("fetching content items, this may take a while...\n")
    pagecontent = _wikipageBuilder.getWikiPage(wiki_title, USER_AGENT)[1]
    _contentItemsHandler.displayitems(pagecontent)
    raise SystemExit(0)
if args.get("contents") != None:
    print("fetching content item text, this may take a while...\n")
    pagecontent = _wikipageBuilder.getWikiPage(wiki_title, USER_AGENT, makePretty=isPretty)[1]
    _contentItemsHandler.displayItemContent(args.get("contents"), pagecontent, usingPaginatedFormat)
    raise SystemExit(0)

if usingFullPage or usingInfoBox:
    print("fetching full html page...")

if usingInfoBox:
    pageContent = _wikipageBuilder.getWikiPage(wiki_title, USER_AGENT, makePretty=False)[1]
    infoboxName = _prettifyPage.getInfoboxName(pageContent)
    # infoboxContent = re.search(r"(?:\{\{Infobox.*?\n)(?P<box>\|.*?(?=\n\}\}))", pageContent, re.DOTALL).group("box")
    infoboxContent = _prettifyPage.getInfoboxContent(pageContent)
    if isCleanDisplay:
        infoboxContent = _cleantextHandler.removeSelected(infoboxContent, cites=args.get("no_cites"), hatnotes=args.get("no_hatnotes"))
    if isSearchingForText:
        _findInPage.displayMatches(infoboxContent, args.get("find"), args.get("no_highlight"))
        raise SystemExit(0)
    wiki_page = f"{infoboxName}\n{infoboxContent}"
    if usingPaginatedFormat:
        pydoc.pager(wiki_page)
        raise SystemExit(0)
    print(wiki_page)
    raise SystemExit(0)

if usingFullPage:
    pageContent = _wikipageBuilder.getWikiPage(wiki_title, USER_AGENT, makePretty=isPretty)[1]
    if isCleanDisplay:
        pageContent = _cleantextHandler.removeSelected(pageContent, cites=args.get("no_cites"), hatnotes=args.get("no_hatnotes"))
    if isSearchingForText:
        _findInPage.displayMatches(pageContent, args.get("find"), args.get("no_highlight"))
        raise SystemExit(0)
    if usingPaginatedFormat:
        pydoc.pager(pageContent)
    else:
        print(pageContent)
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
    wiki_page += "\nRelated Topics:\n{}".format('-'*len("Related Topics:"))
    lastTopicLength = 0
    for topic, description in related_json.items():
        wiki_page += "\n* {} - {}".format(topic, description)
        lastTopicLength = len(str(topic)) + len(str(description)) + 5
    wiki_page += "\n{}\n".format('-'*lastTopicLength)

wiki_page += f"\n\nThis page was last edited on {improved_timestamp}"

if isCleanDisplay:
    wiki_page = _cleantextHandler.removeSelected(wiki_page, cites=args.get("no_cites"), hatnotes=args.get("no_hatnotes"))

if isSearchingForText:
    _findInPage.displayMatches(wiki_page, args.get("find"), args.get("no_highlight"))
    raise SystemExit(0)

loadingbar.complete()
print_loadingProgress("wikipedia page loaded successfully", end='\n')


if usingPaginatedFormat:
    pydoc.pager(wiki_page)
    raise SystemExit(0)
else:
    print(wiki_page)
    raise SystemExit(0)
