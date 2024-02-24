import re

def searchPage(pageData: str, matchString: str) -> str:
    text_found = ''
    for line in pageData.splitlines():
        if bool(re.search(rf"(?:{matchString})", line)):
            text_found += line + '\n'
    return text_found

def displayMatches(text: str, textToFind: str, no_highlight=False) -> str:
    findInPageList = textToFind.split(' ')
    for s in findInPageList:
        text_found = searchPage(text, s)
        if text_found == '':
            raise SystemExit("no matching text found")
        else:
            if not no_highlight:
                text_found = re.sub(rf"(?P<match>{s})", r"\033[31m\g<match>\033[0m", text_found)
            print(text_found)
