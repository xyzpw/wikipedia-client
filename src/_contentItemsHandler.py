import re
import pydoc

def finditems(content: str) -> list:
    finditemsCompiler = re.compile(r"(?<!=)(?:==(?:\s)?)(?P<item>\w+)(?:(?:\s)?==)(?!=)", re.DOTALL)
    items = finditemsCompiler.findall(content)
    return items

def findItemContent(contentTitle: str, contentText: str) -> str:
    # findcontentCompiler = re.compile(r"^(?:(?<!=)==\s?)(?:\w*?)(?:\s?==)$\n(?P<content>.*?)^(?===\s?\w*?\s?==$)", re.DOTALL | re.MULTILINE)
    findcontentCompiler = re.compile(rf"^(?:(?<!=)==\s?)(?:{contentTitle})(?:\s?==)$\n(?P<content>.*?)^(?===\s?\w*?\s?==$)", re.DOTALL | re.MULTILINE)
    itemcontent = findcontentCompiler.search(contentText)
    if itemcontent == None:
        raise SystemExit("no content found")
    return itemcontent.group("content")

def displayitems(content: str):
    items = finditems(content)
    if items == '':
        raise SystemExit("no items found")
    for i in items:
        print(i)

def displayItemContent(contentTitle: str, contentText: str, usePager=False):
    itemcontent = findItemContent(contentTitle, contentText)
    if itemcontent == '':
        raise SystemExit("no text content found")
    if usePager:
        pydoc.pager(itemcontent)
    else:
        print(itemcontent)
