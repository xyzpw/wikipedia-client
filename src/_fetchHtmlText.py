import bs4
import requests

def html2txt(html: str) -> str:
    txt = bs4.BeautifulSoup(html, features="html5lib").get_text()
    return txt

#NOTE: deprecated
def htmlToWikiText(html: str, useragent: str = None) -> str:
    wikipedia_transformedHtml = requests.post("https://en.wikipedia.org/api/rest_v1/transform/html/to/wikitext",
        headers={"user-agent": useragent},
        data={"html": html, "scrub_wikitext": "true"}
    )
    return wikipedia_transformedHtml.text
