import requests
import json

def getPages(title: str, useragent: str):
    apicall = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/related/{title}", headers={"user-agent": useragent})
    wiki_related = json.loads(apicall.text)
    pages_json = {}
    for page in wiki_related['pages']:
        page_title = page.get("title")
        page_description = page.get("description")
        pages_json[page_title] = page_description
    return pages_json
