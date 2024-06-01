import re

#https://en.wikipedia.org/wiki/Wikipedia:Hatnote#Hatnote_templates

def hatnoteExist(hatnoteName, pageContent) -> bool:
    if bool(re.search(r"(?:\{\{"+hatnoteName+r"(?:.*?)\}\})", pageContent, re.DOTALL)):
        return True
    return False

def hatnoteIsEmpty(hatnoteName, pageContent) -> bool:
    if bool(re.search(r"(?:\{\{"+hatnoteName+r"(?:.*?)\}\})", pageContent, re.DOTALL)):
        return True
    return False

def hatnoteMissing(hatnoteName, pageContent) -> bool:
    if not hatnoteExist(hatnoteName, pageContent):
        return True
    if not hatnoteIsEmpty(hatnoteName, pageContent):
        return True
    return False

def lookupHatnoteContent(hatnoteName, pageContent) -> str:
    content = re.search(r"(?:(?<=\{\{)"+hatnoteName+r")(?:.*?)(?=\}\})", pageContent, re.DOTALL)
    if bool(content):
        return content.group(0)
    return None

def hatnotePipeCount(hatnoteName, pageContent):
    if hatnoteMissing(hatnoteName, pageContent):
        return -1
    return lookupHatnoteContent(hatnoteName, pageContent).count('|')

def aboutHatnoteText(pageTitle, pageContent) -> str:
    aboutDistinguished = re.search(r"\{\{about-distinguish\|(?P<use>.*?)\|(?P<page>.*?)\}\}", pageContent, flags=(re.DOTALL | re.IGNORECASE))
    if bool(aboutDistinguished):
        aboutInfoUse = aboutDistinguished.group("use")
        aboutInfoPage = aboutDistinguished.group("text")
        aboutInfoText = f"This page is about {aboutInfoUse}. It is not to be confused with {aboutInfoPage}."
        return aboutInfoText
    aboutInfo = re.search(r"\{\{(?:A|a)bout\|(?P<info>.*?)(?=\|other uses\}\}|\}\})", pageContent, re.DOTALL)
    if bool(aboutInfo):
        aboutInfo = aboutInfo.group("info")
    else:
        return ''
    aboutInfo = aboutInfo.split('|')
    aboutText = f"This article is about {aboutInfo[0]}."
    aboutInfo.pop(0)
    for i in aboutInfo:
        if len(aboutInfo)%2 != 0 or aboutInfo == []:
            break
        aboutText += f" For {aboutInfo[0]}, see {aboutInfo[1]}."
        aboutInfo.pop(0); aboutInfo.pop(0)
    aboutText += f" For other uses, see {pageTitle} (disambiguation)."
    return aboutText

def removeShortDescription(pageContent) -> str:
    shortDescriptionCompiler = re.compile(r"(?:\{\{short description\|(?:.*?)\}\})", flags=(re.DOTALL | re.IGNORECASE))
    if bool(shortDescriptionCompiler.search(pageContent)):
        hatnoteMatch = shortDescriptionCompiler.search(pageContent).group(0)
        pageContent = pageContent.replace(hatnoteMatch, '')
    return pageContent

def replaceMainHatnotes(pageContent) -> str:
    pageContent = re.sub(r"\{\{main\|(?P<article>[\w\s\-\_]*?)\}\}", r"Main article: \g<article>", pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{main\|(?P<article1>.*?)\|(?P<article2>.*?)\}\}", r"Main articles: \g<article1> and \g<article2>", pageContent, flags=(re.DOTALL | re.IGNORECASE))
    return pageContent

#not perfect (limited)
def removeFiles(pageContent) -> str:
    return re.sub(r"\[\[file:[^\[]*?\]\]", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))

def distinguishHatnoteText(pageContent) -> str:
    distinguishedInfo = re.search(r"\{\{distinguish\|(?P<txt>.*?)\}\}", pageContent, flags=(re.DOTALL | re.IGNORECASE))
    if not bool(distinguishedInfo):
        return ''
    distinguishedArray = distinguishedInfo.group("txt").split('|')
    distinguishText = "Not to be confused with "
    distinguishText += distinguishedArray[0]
    if len(distinguishedArray) == 1:
        return str(distinguishText) + str('.')
    distinguishedArray.pop(0)
    for i in distinguishedArray:
        if distinguishedArray.index(i) + 1 == len(distinguishedArray):
            distinguishText += f" or {i}."
            break
        distinguishText += f", {i}"
    return distinguishText

def forHatnoteText(pageContent) -> str:
    forHatnoteSearch = re.search(r"\{\{for\|(?P<for>.*?)\|(?P<see>.*?)\}\}", pageContent, flags=(re.DOTALL | re.IGNORECASE))
    if not bool(forHatnoteSearch):
        return ''
    forHatnoteFor = forHatnoteSearch.group("for")
    forHatnoteSee = forHatnoteSearch.group("see")
    return f"For {forHatnoteFor}, see {forHatnoteSee}."

def replaceFurtherHatnotes(pageContent) -> str:
    return re.sub(r"\{\{further\|(?P<info>.*?)\}\}", r"Further information: \g<info>", pageContent, flags=(re.DOTALL | re.IGNORECASE))
