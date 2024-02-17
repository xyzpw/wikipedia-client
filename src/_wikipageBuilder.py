import requests
import json
import re
from src import _fetchHtmlText
from src import _prettifyPage

wiki_params = {
    "action": "query",
    "format": "json",
    "prop": "revisions",
    "titles": "",
    "formatversion": "2",
    "rvprop": "content",
}

def findRedirect(pageContent) -> str | None:
    redirectSearch = re.search(r"\A#redirect\s?\[\[(?P<page>.*?)\]\]", pageContent, flags=(re.IGNORECASE))
    if bool(redirectSearch):
        return redirectSearch.group("page")
    return None

def getWikiPage(title: str, useragent: str = '', makePretty=True, isRedirect=False) -> tuple:
    endpoint_parameters = {key: title if key == "titles" else var for key, var in wiki_params.items()}
    apicall = requests.get("https://en.wikipedia.org/w/api.php", params=endpoint_parameters,
        headers={
            "user-agent": useragent,
        })
    apicall_json = json.loads(apicall.text)
    try:
        wikipage_title = apicall_json["query"]["pages"][0]["title"]
        wikipage_content = apicall_json["query"]["pages"][0]["revisions"][0]["content"]
    except:
        raise SystemExit("could not find or redirect to wiki page")
    if wikipage_content.lower().startswith("#redirect"):
        new_title = findRedirect(wikipage_content)
        if new_title == None:
            raise SystemExit("could not find or redirect to wiki page")
        return getWikiPage(new_title, useragent, makePretty, isRedirect=True)
    wikipage_content = _fetchHtmlText.html2txt(wikipage_content)
    if isRedirect:
        wikipage_content = f"(Redirected to {title})\n{wikipage_content}"
    if makePretty:
        wikipage_content = _prettifyPage.makePretty(title, wikipage_content)
    return wikipage_title, wikipage_content
